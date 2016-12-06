import unittest
import mock

from brew_control_client.actuator import Actuator
from brew_control_client.brew_state import BrewState
from brew_control_client.controller import BangBangController


class TestBangBangController(unittest.TestCase):


    def setUp(self):

        self._actuator = mock.Mock(spec_set=Actuator)
        self._deadband_width = .1

        self._setpoint = 1.0
        self._brew_state = 1.0

        self._controller = BangBangController(self._actuator, self._extract_actual, self._deadband_width)
        self._d_controller = BangBangController(
            self._actuator,
            self._extract_actual,
            self._deadband_width,
            memory_time_seconds=.1,
            derivative_deadband_width=None
        )

        self._controller.set_setpoint(self._setpoint)
        self._d_controller.set_setpoint(self._setpoint)

    def test_control_actuates_when_actual_less_than_setpoint_without_derivative_control(self):
        state = self._setpoint - 1e-9 - .5*self._deadband_width
        self._controller.control(state)
        self._actuator.actuate.assert_called_once_with(state)

    def test_control_deactuates_when_actual_greater_than_setpoint_without_derivative_control(self):
        state = self._setpoint + 1e-9 + .5*self._deadband_width
        self._controller.control(state)
        self._actuator.deactuate.assert_called_once_with(state)

    def test_control_actuates_when_falling_in_derivative_deadband(self):
        self.fail()

    def test_control_deactuationes_when_rising_in_derivative_deadband(self):
        self.fail()

    def test_control_actuates_when_actual_less_than_setpoint_with_derivative_control(self):
        self.fail()

    def test_control_deactuates_when_actual_greater_than_setpoint_with_derivative_control(self):
        self.fail()

    def test_control_remembers_on_first_call(self):
        self.fail()

    def test_control_does_not_remember_state_before_memory_time(self):
        self.fail()

    def test_control_remembers_state_after_memory_time(self):
        self.fail()

    def _get_critical_low_setpoint(self):
        return self._actual + .5*self._deadband_width

    def _get_critical_high_setpoint(self):
        return self._actual - .5*self._deadband_width

    def _extract_actual(self, brew_state):
        return brew_state


