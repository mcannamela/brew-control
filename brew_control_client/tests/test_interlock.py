import unittest

from interlock import HEXInterlock
from brew_state import BrewState


class TestHEXInterlock(unittest.TestCase):

    def setUp(self):
        self._flowrate_threshold = 2.5
        self._low_temp_threshold = 1.0
        self._high_temp_threshold = 10.0
        self._interlock = HEXInterlock(self._flowrate_threshold,
                                       self._low_temp_threshold,
                                       self._high_temp_threshold)

        self._brew_state = BrewState(
            1e6,
                1e6,
                5.0,
                6.0,
                False,
                False,
            None

        )

    def test_may_actuate_false_for_low_flow(self):
        self._brew_state.pump_outlet_flowrate = self._flowrate_threshold - 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_false_for_low_temp(self):
        self._brew_state.hex_interlock_temperature = self._low_temp_threshold - 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_false_for_high_temp(self):
        self._brew_state.hex_interlock_temperature = self._high_temp_threshold + 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_true(self):
        self.assertTrue(self._interlock.may_actuate(self._brew_state))

    def test_may_deactuate(self):
        self.assertTrue(self._interlock.may_deactuate('blah'))

