import time


class Controller(object):

    def __init__(self, actuator, extract_actual_fun, memory_time_seconds=30.0):

        self._actuator = actuator
        self._extract_actual_fun = extract_actual_fun
        self._setpoint = None
        self._last_state = None
        self._last_time = None
        self._memory_time_seconds = memory_time_seconds

    def control(self, brew_state):
        self._remember_state_if_necessary(brew_state)

        if self._should_actuate(brew_state):
            self._actuate(brew_state)
        else:
            self._handle_should_not_actuate(brew_state)

    def set_setpoint(self, setpoint):
        self._setpoint = setpoint

    def get_setpoint(self):
        return self._setpoint

    def get_actual(self, brew_state):
        return self._extract_actual_fun(brew_state)

    def _remember_state_if_necessary(self, brew_state):
        if self._should_remember_state():
            self._last_state = brew_state
            self._last_time = time.time()

    def _should_remember_state(self):
        if self._last_time is None:
            return True
        else:
            return (time.time() - self._last_time) > self._memory_time_seconds

    def _actuate(self, brew_state):
        self._actuator.actuate(brew_state)

    def _should_actuate(self, brew_state):
        raise NotImplementedError()

    def _handle_should_not_actuate(self, brew_state):
        pass


class BangBangController(Controller):

    def __init__(self, actuator, extract_actual_fun, deadband_width, memory_time_seconds=30.0, derivative_deadband_width=None):
        self._deadband_width = deadband_width
        self._derivative_deadband_width = derivative_deadband_width

        self._raise_if_deadbands_negative()

        super(BangBangController, self).__init__(actuator, extract_actual_fun, memory_time_seconds=memory_time_seconds)

    def _should_actuate(self, brew_state):
        actual = self.get_actual(brew_state)

        if self._has_derivative_control():
            rising_and_dead = self._is_rising(actual)  and self._is_in_derivative_deadband(actual)
            falling_and_dead = self._is_falling(actual) and self._is_in_derivative_deadband(actual)
            below_derivative_deadband = self._is_below_derivative_deadband(actual)
            if rising_and_dead:
                return False
            elif falling_and_dead or below_derivative_deadband:
                return True

        below_deadband = self._is_below_deadband(actual)
        return below_deadband

    def _handle_should_not_actuate(self, brew_state):
        self._actuator.deactuate(brew_state)

    def _is_above_derivative_deadband(self, actual):
        return actual > (self.get_setpoint() + .5*self._derivative_deadband_width)

    def _is_below_derivative_deadband(self, actual):
        return actual < (self.get_setpoint() - .5*self._derivative_deadband_width)

    def _is_above_deadband(self, actual):
        return actual > (self.get_setpoint() + .5*self._deadband_width)

    def _is_below_deadband(self, actual):
        return actual < (self.get_setpoint() - .5*self._deadband_width)

    def _has_derivative_control(self):
        has_derivative_control = self._derivative_deadband_width is not None
        return has_derivative_control

    def _is_rising(self, actual):
        if self._last_state is None:
            return False
        else:
            return actual > self._get_last_actual()

    def _is_falling(self, actual):
        if self._last_state is None:
            return False
        else:
            return not self._is_rising(actual)

    def _raise_if_deadbands_negative(self):
        if self._deadband_width < 0:
            raise RuntimeError("Deadband width must be positive")

        has_derivative_control = self._has_derivative_control()
        if has_derivative_control and self._derivative_deadband_width < 0:
            raise RuntimeError("Deriviative deadband width must be positive")

    def _get_last_actual(self):
        return self.get_actual(self._last_state)

    def _is_in_derivative_deadband(self, actual):
        s = self.get_setpoint()
        w = self._derivative_deadband_width*.5
        return s-w <= actual < s+w


def extract_hlt_actual(brew_state):
    return brew_state.hlt_temperature


def extract_hex_actual(brew_state):
    return brew_state.hex_outlet_temperature