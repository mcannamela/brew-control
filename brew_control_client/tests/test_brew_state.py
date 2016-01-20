import unittest

from brew_state import RawState


class TestRawState(unittest.TestCase):
    def setUp(self):
        self._json_state = {
            RawState._DIGITAL_KEY: [True, False, True],
            RawState._ANALOG_KEY: [1.2, 3.4],
            RawState._INTERRUPT_KEY: [5.6, 7.8]
        }

        self._state = RawState(self._json_state)

    def test_get_digital_state(self):
        self.assertEqual(self._state.get_digital_state(), [True, False, True])

    def test_get_analog_state(self):
        self.fail()

    def test_get_interrupt_state(self):
        self.fail()

class TestBrewState(unittest.TestCase):
    pass

class TestBrewStateFactory(unittest.TestCase):
    pass