import unittest
import mock

from actuator import Actuator
from brew_state import BrewState
from controller import BangBangController


class TestBangBangController(unittest.TestCase):


    def setUp(self):

        self._actuator = mock.Mock(spec_set=Actuator)
        self._actual = 1.0
        self._extract_actual_fun = mock.Mock(return_value=self._actual)
        self._deadband_width = .1

        self._brew_state = mock.Mock(spec_set=BrewState)

        self._controller = BangBangController(self._actuator, self._extract_actual_fun, self._deadband_width)

    def test_control_actuates_when_actual_less_than_setpoint(self):
        self._controller.set_setpoint(self._get_critical_setpoint() + 1e-9)
        self._controller.control(self._brew_state)
        self._actuator.actuate.assert_called_once_with(self._brew_state)

    def test_control_deactuates_when_actual_greater_than_setpoint(self):
        self._controller.set_setpoint(self._get_critical_setpoint() - 1e-9)
        self._controller.control(self._brew_state)
        self._actuator.deactuate.assert_called_once_with(self._brew_state)

    def _get_critical_setpoint(self):
        return self._actual + self._deadband_width

    def _extract_actual(self, brew_state):
        return self._actual

