import unittest

from brew_control_client.brew_state import BrewState
from brew_control_client.interlock import HEXOverheatingInterlock, PumpCavitationInterlock, FlowrateInterlock


class TestHEXOverheatingInterlock(unittest.TestCase):
    def setUp(self):
        self._low_temp_threshold = 1.0
        self._high_temp_threshold = 10.0
        self._interlock = HEXOverheatingInterlock(
            self._low_temp_threshold,
            self._high_temp_threshold
        )

        self._brew_state = BrewState(
            1e6,
            1e6,
            5.0,
            6.0,
            False,
            False,
            None

        )

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


class TestFlowrateInterlock(unittest.TestCase):
    def setUp(self):
        self._low_flowrate_threshold = 2.5
        self._high_flowrate_threshold = 20.5
        self._interlock = FlowrateInterlock(
            self._low_flowrate_threshold,
            self._high_flowrate_threshold,

        )

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
        self._brew_state.pump_outlet_flowrate = self._low_flowrate_threshold - 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_false_for_high_flow(self):
        self._brew_state.pump_outlet_flowrate = self._high_flowrate_threshold + 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_true(self):
        self.assertTrue(self._interlock.may_actuate(self._brew_state))

    def test_may_deactuate(self):
        self.assertTrue(self._interlock.may_deactuate('blah'))


class TestPumpCavitationInterlock(unittest.TestCase):
    def setUp(self):
        self._low_temp_threshold = 1.0
        self._high_temp_threshold = 10.0
        self._interlock = PumpCavitationInterlock(
            self._low_temp_threshold,
            self._high_temp_threshold
        )

        self._brew_state = BrewState(
            1e6,
            5.0,
            1e6,
            6.0,
            False,
            False,
            None

        )

    def test_may_actuate_false_for_low_temp(self):
        self._brew_state.hex_outlet_temperature = self._low_temp_threshold - 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_false_for_high_temp(self):
        self._brew_state.hex_outlet_temperature = self._high_temp_threshold + 1e-9
        self.assertFalse(self._interlock.may_actuate(self._brew_state))

    def test_may_actuate_true(self):
        self.assertTrue(self._interlock.may_actuate(self._brew_state))

    def test_may_deactuate(self):
        self.assertTrue(self._interlock.may_deactuate('blah'))
