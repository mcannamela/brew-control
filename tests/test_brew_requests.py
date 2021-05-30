import unittest

from brew_control_client.brew_requests import (get_index_response,
                                               get_reserved_response,
                                               get_state_response,
                                               get_index_str,
                                               get_interrupt_pins,
                                               get_pincommand_response,
                                               get_reserved_pins,
                                               get_state)
from brew_control_client.brew_state import RawState


class TestResponsesOK(unittest.TestCase):

    def test_get_index_response(self):
        self._check_response_fun_ok(get_index_response)

    def test_get_state_response(self):
        self._check_response_fun_ok(get_state_response)

    def test_get_reserved_response(self):
        self._check_response_fun_ok(get_reserved_response)

    def test_get_pincommand_response(self):
        self._check_response_fun_ok(get_pincommand_response)

    def _check_response_fun_ok(self, f):
        response = f()
        self.assertTrue(response.ok)


class TestGetState(unittest.TestCase):

    def test_get_state(self):
        state = get_state()
        self.assertTrue(isinstance(state, dict))
        self.assertTrue(RawState._DIGITAL_KEY in state)
        self.assertTrue(RawState._ANALOG_KEY in state)
        self.assertTrue(RawState._INTERRUPT_KEY in state)


class TestGetIndexStr(unittest.TestCase):
    def test_get_index_str(self):
        s = get_index_str()
        self.assertTrue(isinstance(s, basestring))


class TestGetReservedAndInterruptPins(unittest.TestCase):
    def test_get_reserved_pins(self):
        s = get_reserved_pins()
        self._assert_is_list_of_ints(s)

    def test_get_interrupt_pins(self):
        s = get_interrupt_pins()
        self._assert_is_list_of_ints(s)

    def _assert_is_list_of_ints(self, x):
        self.assertTrue(isinstance(x, list))
        self.assertTrue(all([isinstance(i, int) for i in x]))
