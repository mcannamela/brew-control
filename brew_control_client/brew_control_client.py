import logging
import requests
import socket

import time

from actuator import HLTActuator, HEXActuator
from controller import BangBangController, extract_hlt_actual, extract_hex_actual
from interlock import FlowrateInterlock, HEXOverheatingInterlock, PumpCavitationInterlock, HLTThermistorFaultInterlock
from brew_state import BrewStateProvider


class BrewControlClient(object):

    COMM_EXCEPTIONS = (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        socket.timeout,
        socket.error
    )

    def __init__(self,
                 controllers,
                 get_brew_state_fun,
                 setup_fun,
                 loop_delay_seconds=30,
                 hangover_delay_seconds=60,
                 logger=None):
        self._controllers = controllers
        self._get_brew_state_fun = get_brew_state_fun
        self._setup_fun = setup_fun
        self._logger = logger if logger is not None else logging.getLogger('brew_control_client')
        self._loop_delay_seconds = loop_delay_seconds
        self._hangover_delay_seconds = hangover_delay_seconds
        self._last_loop_time = None

    def setup(self):
        self._setup_fun()

    def execute_loop(self):
        brew_state = self._get_brew_state()
        self._logger.info('\n\n')
        self._logger.info(80 * '-')
        self._logger.info(repr(brew_state))
        self._logger.info('\n')
        for c in self._controllers:
            c.control(brew_state)

        self._last_loop_time = time.time()
        return brew_state

    def __iter__(self):
        self.setup()
        while True:
            try:
                try:
                    brew_state = self.execute_loop()
                    yield brew_state
                except self.COMM_EXCEPTIONS as exc:
                    self._handle_communiction_error(exc)
                else:
                    self._delay_if_necessary()
            except KeyboardInterrupt:
                self._logger.info("User demands stopping brew.")
                raise StopIteration

    def _delay_if_necessary(self):
        t = time.time()
        corrected_delay = self._loop_delay_seconds - (t - self._last_loop_time)
        if corrected_delay > 1e-6:
            self._logger.info("Now sleep. Next control action in {} s".format(corrected_delay))
            time.sleep(corrected_delay)
        else:
            self._logger.info("Sleep unnecessary. Taking next control action now!")

    def _handle_communiction_error(self, exc):
        self._logger.error("Trapped ConnectionError or Timeout! Will try to sleep it off: {}".format(exc))
        time.sleep(self._hangover_delay_seconds)
        self.setup()

    def _get_brew_state(self):
        return self._get_brew_state_fun()


class BrewControlClientFactory(object):
    def __init__(self, command_factory, brew_state_factory, brew_server, logger=None):
        self._command_factory = command_factory
        self._brew_state_factory = brew_state_factory
        self._brew_server = brew_server
        self._issue_command_fun = self._brew_server.issue_pin_commands
        self._get_brew_state_fun = BrewStateProvider(self._brew_state_factory,
                                                     self._brew_server.get_raw_state).get_brew_state
        self._logger = logger if logger is not None else logging.getLogger('brew_control_client_factory')

    def __call__(self, hlt_setpoint, hex_setpoint, loop_delay_seconds=30, hangover_delay_seconds=60):
        controllers = self._get_controllers(hlt_setpoint, hex_setpoint)

        return BrewControlClient(
                controllers,
                self._get_brew_state_fun,
                self._setup,
                loop_delay_seconds=loop_delay_seconds,
                hangover_delay_seconds=hangover_delay_seconds,
                logger=self._logger
        )

    def _get_controllers(self, hlt_setpoint, hex_setpoint):
        return [self._get_hlt_controller(hlt_setpoint), self._get_hex_controller(hex_setpoint)]

    def _setup(self):
        command_factory = self._get_command_factory()
        c = command_factory.get_setup_command()
        self._logger.info("Setup the brew control:\n {}".format(repr(c)))
        self._issue_command_fun(c.render_as_request_parameters())

    def _get_hlt_controller(self, setpoint):
        c = BangBangController(
                self._get_hlt_actuator(),
                extract_hlt_actual,
                self._get_deadband_width(),
                memory_time_seconds=self._get_memory_time_seconds(),
        )
        c.set_setpoint(setpoint)
        return c

    def _get_hex_controller(self, setpoint):
        c = BangBangController(
                self._get_hex_actuator(),
                extract_hex_actual,
                self._get_deadband_width(),
                memory_time_seconds=self._get_memory_time_seconds(),
                derivative_tripband_width=self._get_derivative_tripband_width(),
                derivative_threshold=self._get_derivative_threshold(),

        )
        c.set_setpoint(setpoint)
        return c

    def _get_deadband_width(self):
        return .5

    def _get_hlt_actuator(self):
        return HLTActuator(
                self._issue_command_fun,
                self._get_command_factory(),
                self._get_hlt_interlocks(),
                logger=self._logger
        )

    def _get_hex_actuator(self):
        return HEXActuator(
                self._issue_command_fun,
                self._get_command_factory(),
                self._get_hex_interlocks(),
                logger=self._logger
        )

    def _get_command_factory(self):
        return self._command_factory

    def _get_hlt_interlocks(self):
        return [
            HLTThermistorFaultInterlock(
                    self._get_low_thermistor_fault_temp(),
                    self._get_high_hlt_thermistor_fault_temp(),
                    logger=self._logger
            )
        ]

    def _get_hex_interlocks(self):
        return [
            FlowrateInterlock(
                    self._get_low_flowrate_threshold(),
                    self._get_high_flowrate_threshold(),
                    logger=self._logger
            ),
            HEXOverheatingInterlock(
                    self._get_low_thermistor_fault_temp(),
                    self._get_hex_overheat_temp(),
                    logger=self._logger
            ),
            PumpCavitationInterlock(
                    self._get_low_thermistor_fault_temp(),
                    self._get_pump_cavitation_temp(),
                    logger=self._logger
            )
        ]

    def _get_low_flowrate_threshold(self):
        # 2e-3 L/s is about 1 pulse per second
        # we'll cut out when we're down to about 1 pulse every 10 seconds

        #measured 9.6e-4 L/s by hand, after 10 min sensor gave 3e-4 +/- 1e-4, so the reliability is not great at low flows
        return 2e-4

    def _get_high_flowrate_threshold(self):
        # flowrate with HLT only fully open is about .08 L/s, so if it doubles that something is wrong.
        return 0.2

    def _get_low_thermistor_fault_temp(self):
        return 5.0

    def _get_high_hlt_thermistor_fault_temp(self):
        return 100.0

    def _get_hex_overheat_temp(self):
        return 95.0

    def _get_pump_cavitation_temp(self):
        return 70.0

    def _get_deadband_width(self):
        return 1.0

    def _get_derivative_tripband_width(self):
        return None

    def _get_derivative_threshold(self):
        return .2

    def _get_memory_time_seconds(self):
        return 15.0
