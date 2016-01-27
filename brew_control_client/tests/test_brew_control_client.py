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
        pin_config = PinConfig()
        thermistors_by_pin = {pin: Thermistor(divider_resistance)
                              for pin, divider_resistance in THERMISTOR_RESISTANCES.items()
                              }
        flowrate_sensor = FlowrateSensor(FLOWRATE_SENSOR_LITERS_PER_PULSE)

        brew_state_factory = BrewStateFactory(pin_config, thermistors_by_pin, flowrate_sensor)
        brew_server = FakeServer(RESERVED_PINS, INTERRUPT_PINS)
        command_factory = CommandFactory(pin_config)

        self.client_factory = BrewControlClientFactory(command_factory,
                                 brew_state_factory,
                                 brew_server,
                                 )
        self.hlt_setpoint = 75.0
        self.hex_setpoint = 66.6
        self.client = self.client_factory(
                self.hlt_setpoint,
                self.hex_setpoint,
                loop_delay_seconds=.01,
                hangover_delay_seconds=.1
        )

    def test_hex_actuates_when_below_setpoint(self):
        self.fail()

    def test_hlt_actuates_when_below_setpoint(self):
        self.fail()

    def test_hex_deactuates_when_above_setpoint(self):
        self.fail()

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

    def test_hlt_deactuates_on_low_hlt_thermistor_fault(self):
        self.fail()

