import unittest

from brew_requests import get_reserved_pins, get_interrupt_pins
from pin_config import PinConfig


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

    def test_interrupt_pins_are_reserved(self):
        reserved_pins = set(get_reserved_pins())
        interrupt_pins = set(get_interrupt_pins())
        self.assertTrue(interrupt_pins <= reserved_pins)

