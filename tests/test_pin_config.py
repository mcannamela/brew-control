import unittest

from brew_control_client.brew_requests import get_reserved_pins, get_interrupt_pins
from brew_control_client.pin_config import PinConfig, THERMISTOR_RESISTANCES, RESERVED_PINS, INTERRUPT_PINS


class TestPinConfig(unittest.TestCase):

    def setUp(self):
        self._pin_config = PinConfig()

    def test_actuation_pins_not_reserved(self):
        reserved_pins = set(get_reserved_pins())
        self.assertFalse(self._pin_config.HEX_actuation_pin in reserved_pins)
        self.assertFalse(self._pin_config.HLT_actuation_pin in reserved_pins)

    def test_flowrate_pin_is_interrupt(self):
        interrupt_pins = set(get_interrupt_pins())
        self.assertTrue(self._pin_config.flow_interrupt_pin in interrupt_pins)

    def test_flowrate_pin_index_matches(self):
        interrupt_pins = get_interrupt_pins()
        self.assertEqual(interrupt_pins.index(self._pin_config.flow_interrupt_pin),
                         self._pin_config.flow_interrupt_pin_index)

    def test_interrupt_pins_are_reserved(self):
        reserved_pins = set(get_reserved_pins())
        interrupt_pins = set(get_interrupt_pins())
        self.assertTrue(interrupt_pins <= reserved_pins)


class TestReservedAndInterruptPins(unittest.TestCase):

    def test_reserved_pins(self):
        reserved_pins = set(get_reserved_pins())
        self.assertEqual(set(RESERVED_PINS), reserved_pins)

    def test_interrupt_pins(self):
        interrupt_pins = set(get_interrupt_pins())
        self.assertEqual(set(INTERRUPT_PINS), interrupt_pins)


class TestThermistorDividerResistances(unittest.TestCase):

    def setUp(self):
        self._pin_config = PinConfig()

    def test_all_pins_accounted_for(self):
        self.assertTrue(isinstance(THERMISTOR_RESISTANCES, dict))
        self.assertTrue(self._pin_config.HLT_thermistor_pin in THERMISTOR_RESISTANCES)
        self.assertTrue(self._pin_config.HEX_outlet_thermistor_pin in THERMISTOR_RESISTANCES)
        self.assertTrue(self._pin_config.HEX_interlock_thermistor_pin in THERMISTOR_RESISTANCES)
