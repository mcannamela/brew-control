import time
import unittest

import mock
import numpy as np
import pylab
from scipy.ndimage.filters import convolve1d

from brew_control_client.actuator import Actuator
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
        state = self._setpoint + .5 * self._derivative_trip_band_width - self._small
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
        time.sleep(self._memory_time_seconds / 5.0)
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


class FakeTankAndHeater(object):

    def __init__(self, mass, mass_flowrate, mixing_time, heating_temperature_difference, cooling_temperature_difference,
                 initial_temperature, control_interval):
        self._mass = mass
        self._mass_flowrate = mass_flowrate
        self._mixing_time = mixing_time
        self._heating_temperature_difference = heating_temperature_difference
        self._cooling_temperature_difference = cooling_temperature_difference
        self._initial_temperature = initial_temperature
        self._control_interval = control_interval

        self.is_heating = False
        self.time = None
        self.temperature = None
        self._idx = None
        self._kernel = None

        self._init_mesh_and_temperature()

    def set_mass(self, mass):
        self._mass = mass
        self._init_mesh_and_temperature()

    def set_mass_flowrate(self, mass_flowrate):
        self._mass_flowrate = mass_flowrate
        self._init_mesh_and_temperature()

    def set_mixing_time(self, mixing_time):
        self._mixing_time = mixing_time
        self._init_mesh_and_temperature()

    def set_heating_temperature_difference(self, x):
        self._heating_temperature_difference = x

    def set_cooling_temperature_difference(self, x):
        self._cooling_temperature_difference = x

    def actuate(self, brew_state):
        self.is_heating = True

    def deactuate(self, brew_state):
        self.is_heating = False

    def get_output_state(self):
        return self.temperature[-1]

    def get_input_state(self):
        if self.is_heating:
            return self.get_output_state() + self._heating_temperature_difference
        else:
            return self.get_output_state() - self._cooling_temperature_difference

    def update(self):
        self._advect()
        self._diffuse()

    def get_dwell_time(self):
        return self._mass / self._mass_flowrate

    def _advect(self):
        input = self.get_input_state()
        self.temperature[self._idx] = self.temperature[self._idx - 1]
        self.temperature[0] = input

    def _diffuse(self):
        new_temp = convolve1d(self.temperature, self._get_kernel(), mode='reflect')
        self.temperature = new_temp

    def _init_time_mesh(self):
        n = int(self.get_dwell_time() / self.delta_t)
        t = np.linspace(0, self.get_dwell_time(), n)
        self.time = t

    def _compute_delta_t(self):
        kernel_width = self._get_kernel_width_in_steps()
        dt_from_mixing = self.get_dwell_time() / (5 * kernel_width)
        dt_from_control = self._control_interval / 10.0
        dt = min(dt_from_mixing, dt_from_control)
        return dt

    def _get_kernel_width_in_steps(self):
        r = (self.get_dwell_time() / self._mixing_time)
        n = 10 * r
        if n < 1.0:
            n = 1
        else:
            n = max(int(n), 3)
            if n % 2 == 0:
                n += 1
        return n

    def _get_kernel(self):
        if self._kernel is None:
            w = self._get_kernel_width_in_steps()
            if w == 1:
                self._kernel = np.atleast_1d(np.ones(1))
            else:
                t = np.linspace(-w * .5, w * .5, w) * self.delta_t
                sig = self.delta_t * self.get_dwell_time() / self._mixing_time
                kern = np.exp(-.5 * (t / sig) ** 2)
                kern /= np.sum(kern)
                self._kernel = kern
        return self._kernel

    def _init_mesh_and_temperature(self):
        self.delta_t = self._compute_delta_t()
        self._init_time_mesh()
        self.temperature = np.zeros(len(self.time)) + self._initial_temperature
        self._idx = np.arange(len(self.time))
        self._kernel = None


class Simulation(object):
    def __init__(self, plant, controller, control_interval, increment_time_fun, get_time_fun):
        self._plant = plant
        self._controller = controller
        self._control_interval = control_interval
        self._increment_time_fun = increment_time_fun
        self._get_time_fun = get_time_fun

    def set_control_interval(self, dt):
        self._control_interval = dt

    def simulate(self, n_dwell_times=10):
        dt = self._plant.delta_t
        n = int(n_dwell_times * self._plant.get_dwell_time() / dt)
        n_control = int(self._control_interval / dt)
        t = np.zeros(n)
        temperature = np.zeros(n)
        actuated = np.zeros(n, dtype=bool)

        for i in range(n):
            t[i] = self._get_time_fun()
            this_temperature = self._plant.get_input_state()
            temperature[i] = this_temperature
            actuated[i] = self._plant.is_heating
            if i % n_control == 0:
                self._controller.control(this_temperature)
            self._plant.update()
            self._increment_time_fun(dt)

        return t, temperature, actuated


class TestBangBangControllerInSimulation(unittest.TestCase):
    def setUp(self):
        self._control_interval = 1.0
        # 20/.067 gives a dwell time of 300s
        self._plant = FakeTankAndHeater(
            20.0,
            .067,  # about 1 gal per minute
            10.0,
            1.0,
            1.0,
            1.5,
            self._control_interval
        )

        self._deadband_width = 1.0
        self._derivative_tripband_width = .6
        self._controller = BangBangController(
            self._plant,
            self._extract_actual,
            memory_time_seconds=30.0,
            derivative_tripband_width=self._derivative_tripband_width,
            deadband_width=self._deadband_width,
            derivative_threshold=0.1
        )
        self._controller.set_setpoint(0.0)

        self._time = 0.0

        self._simulation = Simulation(
            self._plant,
            self._controller,
            self._control_interval,
            self._increment_time,
            self._get_time
        )

    def test_well_mixed_massless_system(self):
        temperature_difference = self._derivative_tripband_width / 3.0
        self._plant.set_mass_flowrate(20.0)
        self._plant.set_mixing_time(1.0)
        self._plant.set_heating_temperature_difference(temperature_difference)
        self._plant.set_cooling_temperature_difference(temperature_difference)
        self._simulation.set_control_interval(.1)
        self._controller.set_memory_time_seconds(1.0)

        t, temperature, actuated = self._simulation.simulate()

        # pylab.plot(t, temperature, 'k')
        # pylab.plot(t, actuated, 'r')
        # pylab.show()

        self._assert_at_least_last_half_in_deadband(temperature, atol=temperature_difference)

    def test_poorly_mixed_massive_system(self):
        temperature_difference = .2123
        self._plant.set_mixing_time(1e6)
        self._plant.set_heating_temperature_difference(temperature_difference)
        self._plant.set_cooling_temperature_difference(temperature_difference)
        self._simulation.set_control_interval(.5)
        self._controller.set_memory_time_seconds(10.0)

        # # with no mixing whatsoever, the derivative control can be very sensitive
        # self._controller.set_derivative_tripband_width(None)

        t, temperature, actuated = self._simulation.simulate(n_dwell_times=20)

        # pylab.plot(t, actuated, 'r')
        # pylab.plot(t, temperature, 'k')
        # pylab.show()

        self._assert_at_least_last_half_in_deadband(temperature, atol=temperature_difference)

    def _extract_actual(self, brew_state):
        return brew_state

    def _get_time(self):
        return self._time

    def _increment_time(self, dt):
        self._time += dt

    def _assert_at_least_last_half_in_deadband(self, temperature, atol=None):
        first_in = np.flatnonzero(self._in_deadband_mask(temperature, atol=atol))[0]
        self.assertLess(first_in, len(temperature) / 2)
        self.assertTrue(np.all(self._in_deadband_mask(temperature[first_in:], atol=atol)))

    def _in_deadband_mask(self, temperature, atol=None):
        t = self._deadband_width * .55 if atol is None else (self._deadband_width * .5 + atol)
        setpoint = self._controller.get_setpoint()
        return np.abs(temperature - setpoint) < t
