import unittest

from brew_state import RawState


class TestRawState(unittest.TestCase):
    def setUp(self):
        self._digital_state = [True, False, True]
        self._analog_state = [1.2, 3.4]
        self._interrupt_state = [5.6, 7.8]
        self._json_state = {
            RawState._DIGITAL_KEY: self._digital_state,
            RawState._ANALOG_KEY: self._analog_state,
            RawState._INTERRUPT_KEY: self._interrupt_state
        }

        self._state = RawState(self._json_state)

    def test_get_digital_state(self):
        self.assertEqual(self._state.get_digital_state(), self._digital_state)

    def test_get_analog_state(self):
        self.assertEqual(self._state.get_analog_state(), self._analog_state)

    def test_get_interrupt_state(self):
        self.assertEqual(self._state.get_interrupt_state(), self._interrupt_state)

class TestBrewState(unittest.TestCase):
    pass

class TestBrewStateFactory(unittest.TestCase):
    pass