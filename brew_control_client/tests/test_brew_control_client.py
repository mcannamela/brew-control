import unittest
from pin_config import PinConfig, THERMISTOR_RESISTANCES, FLOWRATE_SENSOR_LITERS_PER_PULSE, RESERVED_PINS, INTERRUPT_PINS
from thermistor import Thermistor
from flowrate_sensor import FlowrateSensor
from brew_state import BrewStateFactory
from fake_server import FakeServer
from pin_command import CommandFactory
from brew_control_client import BrewControlClientFactory


class BrewControlClientTest(unittest.TestCase):

    def setUp(self):
        self._analog_value_204_c = 7.0
        self._analog_value_91_c = 85.0
        self._analog_value_40_c = 355.0
        self._analog_value_1_c = 779.0


        self.pin_config = PinConfig()
        thermistors_by_pin = {pin: Thermistor(divider_resistance)
                              for pin, divider_resistance in THERMISTOR_RESISTANCES.items()
                              }
        flowrate_sensor = FlowrateSensor(FLOWRATE_SENSOR_LITERS_PER_PULSE)

        self.brew_state_factory = BrewStateFactory(self.pin_config, thermistors_by_pin, flowrate_sensor)
        command_factory = CommandFactory(self.pin_config)
        self.brew_server = FakeServer(RESERVED_PINS, INTERRUPT_PINS)

        self.client_factory = BrewControlClientFactory(command_factory,
                                 self.brew_state_factory,
                                 self.brew_server,
                                 )
        self.hlt_setpoint = 75.0
        self.hex_setpoint = 66.6
        self.client = self.client_factory(
                self.hlt_setpoint,
                self.hex_setpoint,
                loop_delay_seconds=.01,
                hangover_delay_seconds=.1
        )

        self.client.setup()

        self._set_hex_below_setpoint()
        self._set_hlt_below_setpoint()
        self.brew_server.set_analog_state(self.pin_config.HEX_interlock_thermistor_pin, self._analog_value_91_c)
        self.brew_server.set_digital_state(self.pin_config.HLT_actuation_pin, False)
        self.brew_server.set_digital_state(self.pin_config.HEX_actuation_pin, False)
        self.brew_server.set_interrupt_frequency(self.pin_config.flow_interrupt_pin_index, 1000.0)

    def test_hex_actuates_when_below_setpoint(self):
        self._set_hlt_above_setpoint()

        self._assert_hex_not_actuated()
        self._assert_hlt_not_actuated()

        brew_state = self.client.execute_loop()

        self._assert_hex_actuated()
        self._assert_hlt_not_actuated()

    def test_hlt_actuates_when_below_setpoint(self):
        self._set_hex_above_setpoint()

        self._assert_hex_not_actuated()
        self._assert_hlt_not_actuated()

        brew_state = self.client.execute_loop()

        self._assert_hlt_actuated()
        self._assert_hex_not_actuated()

    def test_hex_deactuates_when_above_setpoint(self):
        self._set_hex_above_setpoint()
        self._set_hex_actuated()
        self._set_hlt_actuated()

        self._assert_hex_actuated()
        self._assert_hlt_actuated()

        brew_state = self.client.execute_loop()

        self._assert_hlt_actuated()
        self._assert_hex_not_actuated()

    def _set_hlt_actuated(self):
        self.brew_server.set_digital_state(self.pin_config.HLT_actuation_pin, True)

    def _set_hex_actuated(self):
        self.brew_server.set_digital_state(self.pin_config.HEX_actuation_pin, True)

    def test_hlt_deactuates_when_above_setpoint(self):
        self.fail()

    def test_hex_deactuates_on_low_hex_thermistor_fault(self):
        self.fail()

    def test_hex_deactuates_on_low_high_hex_thermistor_fault(self):
        self.fail()

    def test_hex_deactuates_on_low_hex_interlock_fault(self):
        self.fail()

    def test_hex_deactuates_on_high_hex_interlock_fault(self):
        self.fail()

    def test_hex_deactuates_on_low_flowrate_fault(self):
        self.fail()

    def test_hex_deactuates_on_high_flowrate_fault(self):
        self.fail()

    def test_hlt_deactuates_on_low_hlt_thermistor_fault(self):
        self.fail()

    def test_hlt_deactuates_on_high_hlt_thermistor_fault(self):
        self.fail()

    def _set_hlt_above_setpoint(self):
        pin = self.pin_config.HLT_thermistor_pin
        self._set_to_high_temp(pin)

    def _set_hlt_below_setpoint(self):
        pin = self.pin_config.HLT_thermistor_pin
        self._set_to_low_temp(pin)

    def _set_hex_above_setpoint(self):
        pin = self.pin_config.HEX_outlet_thermistor_pin
        self._set_to_high_temp(pin)

    def _set_hex_below_setpoint(self):
        pin = self.pin_config.HEX_outlet_thermistor_pin
        self._set_to_low_temp(pin)

    def _set_to_high_temp(self, pin):
        self.brew_server.set_analog_state(pin, self._analog_value_91_c)

    def _set_to_low_temp(self, pin):
        self.brew_server.set_analog_state(pin, self._analog_value_40_c)

    def _set_to_very_high_temp(self, pin):
        self.brew_server.set_analog_state(pin, self._analog_value_204_c)

    def _set_to_very_low_temp(self, pin):
        self.brew_server.set_analog_state(pin, self._analog_value_1_c)

    def _assert_hex_not_actuated(self):
        self.assertFalse(self._get_hex_actuated())

    def _assert_hex_actuated(self):
        self.assertTrue(self._get_hex_actuated())

    def _assert_hlt_not_actuated(self):
        self.assertFalse(self._get_hlt_actuated())

    def _assert_hlt_actuated(self):
        self.assertTrue(self._get_hlt_actuated())

    def _get_hex_actuated(self):
        return self.brew_server.get_digital_state(self.pin_config.HEX_actuation_pin)

    def _get_hlt_actuated(self):
        return self.brew_server.get_digital_state(self.pin_config.HLT_actuation_pin)

