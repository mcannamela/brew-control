import unittest
import mock
import time

from brew_control_client.actuator import Actuator
from brew_control_client.brew_state import BrewState
from brew_control_client.controller import BangBangController


class TestBangBangController(unittest.TestCase):

    def setUp(self):
        self._actuator = mock.Mock(spec_set=Actuator)
        self._deadband_width = .1

        self._setpoint = 1.0

        self._deadband_upper = self._setpoint + .05
        self._deadband_lower = self._setpoint - .05
        self._small = 1e-9

        self._brew_state = 1.0
        self._memory_time_seconds = .1
        self._derivative_threshold = .1
        self._derivative_trip_band_width = .05

        self._controller = BangBangController(
            self._actuator,
            self._extract_actual,
            self._deadband_width,
            memory_time_seconds=self._memory_time_seconds,
            derivative_threshold=self._derivative_threshold
        )
        self._d_controller = BangBangController(
            self._actuator,
            self._extract_actual,
            self._deadband_width,
            memory_time_seconds=self._memory_time_seconds,
            derivative_tripband_width=self._derivative_trip_band_width,
            derivative_threshold=self._derivative_threshold

        )

        self._controller.set_setpoint(self._setpoint)
        self._d_controller.set_setpoint(self._setpoint)

    def test___init__raises_for_negative_deadband(self):
        with self.assertRaises(RuntimeError):
            BangBangController(
                self._actuator,
                self._extract_actual,
                -self._deadband_width,
            )

    def test___init__raises_for_negative_derivative_tripband(self):
        with self.assertRaises(RuntimeError):
            BangBangController(
                self._actuator,
                self._extract_actual,
                self._deadband_width,
                derivative_tripband_width=-1,
            )

    def test___init__raises_for_negative_derivative_threshold(self):
        with self.assertRaises(RuntimeError):
            BangBangController(
                self._actuator,
                self._extract_actual,
                self._deadband_width,
                derivative_threshold=-1,
            )

    def test___init__raises_for_derivative_tripband_larger_than_deadband(self):
        with self.assertRaises(RuntimeError):
            BangBangController(
                self._actuator,
                self._extract_actual,
                self._deadband_width,
                derivative_tripband_width=self._deadband_width,
            )

    def test_control_actuates_below_deadband_without_derivative_control(self):
        state = self._deadband_lower - self._small
        self._controller.control(state)
        self._assert_actuated_once(state)

    def test_control_deactuates_above_deadband_without_derivative_control(self):
        state = self._deadband_upper + self._small
        self._controller.control(state)
        self._assert_deactuated_once(state)

    def test_control_neither_actuates_nor_deactuates_in_deadband_without_derivative_control(self):
        state = self._deadband_upper - self._small
        self._controller.control(state)
        self._assert_no_action_taken()

        state = self._deadband_lower + self._small
        self._controller.control(state)
        self._assert_no_action_taken()

    def test_control_actuates_in_derivative_upper_tripband_when_falling(self):
        self._setup_last_state_for_falling()
        state = self._setpoint + .5*self._derivative_trip_band_width - self._small
        self._d_controller.control(state)
        self._assert_actuated_once(state)

    def test_control_does_not_actuate_in_derivative_lower_tripband_when_falling(self):
        self._setup_last_state_for_falling()
        state = self._setpoint - .5 * self._derivative_trip_band_width + self._small
        self._d_controller.control(state)
        self._assert_no_action_taken()

    def test_control_actuates_below_deadband_when_falling(self):
        self._setup_last_state_for_falling()
        state = self._deadband_lower - self._small
        self._d_controller.control(state)
        self._assert_actuated_once(state)

    def test_control_actuates_below_deadband_when_rising(self):
        self._setup_last_state_for_rising()
        state = self._deadband_lower - self._small
        self._d_controller.control(state)
        self._assert_actuated_once(state)

    def test_control_deactuates_when_rising_in_derivative_lower_tripband(self):
        self._setup_last_state_for_rising()
        state = self._setpoint - .5 * self._derivative_trip_band_width + self._small
        self._d_controller.control(state)
        self._assert_deactuated_once(state)

    def test_control_does_not_deactuate_when_rising_in_derivative_upper_tripband(self):
        self._setup_last_state_for_rising()
        state = self._setpoint + .5 * self._derivative_trip_band_width - self._small
        self._d_controller.control(state)
        self._assert_no_action_taken()

    def test_control_deactuates_above_deadband_when_falling(self):
        self._setup_last_state_for_falling()
        state = self._deadband_upper + self._small
        self._d_controller.control(state)
        self._assert_deactuated_once(state)

    def test_control_deactuates_above_deadband_when_rising(self):
        self._setup_last_state_for_rising()
        state = self._deadband_upper + self._small
        self._d_controller.control(state)
        self._assert_deactuated_once(state)

    def test_control_remembers_on_first_call(self):
        c = self._controller
        self._assert_no_state_remembered(c)
        c.control(self._brew_state)
        self.assertEqual(self._brew_state, c._last_state)
        self.assertFalse(c._last_time is None)

    def test_control_does_not_remember_state_before_memory_time(self):
        self._controller.control(self._brew_state)
        new_state = self._brew_state + 1.0
        time.sleep(self._memory_time_seconds/5.0)
        self._controller.control(new_state)
        self.assertAlmostEqual(self._brew_state, self._controller._last_state)

    def test_control_remembers_state_after_memory_time(self):
        self._controller.control(self._brew_state)
        new_state = self._brew_state
        for i in range(3):
            time.sleep(self._memory_time_seconds)
            new_state += 1.0
            self._controller.control(new_state)
            self.assertAlmostEqual(new_state, self._controller._last_state)

    def test__is_falling_false_without_previous_state(self):
        self._assert_no_state_remembered(self._controller)
        self.assertFalse(self._controller._is_falling(self._brew_state))

    def test__is_falling(self):
        self._controller.control(self._brew_state)
        self.assertFalse(self._controller._is_falling(self._brew_state - self._small))
        self.assertFalse(self._controller._is_falling(self._brew_state - self._derivative_threshold + self._small))
        self.assertTrue(self._controller._is_falling(self._brew_state - self._derivative_threshold - self._small))

    def test__is_rising_false_without_previous_state(self):
        self._assert_no_state_remembered(self._controller)
        self.assertFalse(self._controller._is_rising(self._brew_state))

    def test__is_rising(self):
        self._controller.control(self._brew_state)
        self.assertFalse(self._controller._is_rising(self._brew_state + self._small))
        self.assertFalse(self._controller._is_rising(self._brew_state + self._derivative_threshold - self._small))
        self.assertTrue(self._controller._is_rising(self._brew_state + self._derivative_threshold + self._small))

    def _setup_last_state_for_falling(self):
        last_state = self._setpoint + 1000.0
        self._d_controller.control(last_state)
        self._actuator.reset_mock()
        self._assert_no_action_taken()

    def _setup_last_state_for_rising(self):
        last_state = self._setpoint - 1000.0
        self._d_controller.control(last_state)
        self._actuator.reset_mock()
        self._assert_no_action_taken()

    def _extract_actual(self, brew_state):
        return brew_state

    def _assert_no_state_remembered(self, c):
        self.assertTrue(c._last_state is None)
        self.assertTrue(c._last_time is None)

    def _assert_no_action_taken(self):
        self.assertFalse(self._actuator.actuate.called)
        self.assertFalse(self._actuator.deactuate.called)

    def _assert_actuated_once(self, state):
        self._actuator.actuate.assert_called_once_with(state)
        self.assertFalse(self._actuator.deactuate.called)

    def _assert_deactuated_once(self, state):
        self._actuator.deactuate.assert_called_once_with(state)
        self.assertFalse(self._actuator.actuate.called)


