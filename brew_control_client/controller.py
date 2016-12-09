import time


class Controller(object):

    def __init__(self, actuator, extract_actual_fun, memory_time_seconds=30.0, timefun=time.time):

        self._actuator = actuator
        self._extract_actual_fun = extract_actual_fun
        self._setpoint = None
        self._last_state = None
        self._last_time = None
        self._memory_time_seconds = memory_time_seconds
        self._timefun = timefun

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

    def set_memory_time_seconds(self, t):
        self._memory_time_seconds = t

    def _remember_state_if_necessary(self, brew_state):
        if self._should_remember_state():
            self._last_state = brew_state
            self._last_time = self._timefun()

    def _should_remember_state(self):
        if self._last_time is None:
            return True
        else:
            return (self._timefun() - self._last_time) > self._memory_time_seconds

    def _actuate(self, brew_state):
        self._actuator.actuate(brew_state)

    def _should_actuate(self, brew_state):
        raise NotImplementedError()

    def _handle_should_not_actuate(self, brew_state):
        pass


class BangBangController(Controller):

    def __init__(self,
                 actuator,
                 extract_actual_fun,
                 deadband_width,
                 memory_time_seconds=30.0,
                 derivative_tripband_width=None,
                 derivative_threshold=0.0):
        self._deadband_width = deadband_width
        self._derivative_tripband_width = derivative_tripband_width
        self._derivative_threshold = derivative_threshold

        self._raise_if_bandwidths_negative_or_derivative_band_too_large()

        super(BangBangController, self).__init__(actuator, extract_actual_fun, memory_time_seconds=memory_time_seconds)

    def set_deadband_width(self, w):
        self._deadband_width = w
        self._raise_if_bandwidths_negative_or_derivative_band_too_large()

    def set_derivative_tripband_width(self, w):
        self._derivative_tripband_width = w
        self._raise_if_bandwidths_negative_or_derivative_band_too_large()

    def _should_actuate(self, brew_state):
        actual = self.get_actual(brew_state)

        if self._is_below_deadband(actual):
            return True
        elif self._has_derivative_control():
            falling_and_tripped = self._is_falling(actual) and self._is_in_upper_derivative_tripband(actual)
            if falling_and_tripped:
                return True
        else:
            return False

    def _handle_should_not_actuate(self, brew_state):
        actual = self.get_actual(brew_state)
        if self._is_above_deadband(actual):
            self._actuator.deactuate(brew_state)
        elif self._has_derivative_control():
            rising_and_tripped = self._is_rising(actual) and self._is_in_lower_derivative_tripband(actual)
            if rising_and_tripped:
                self._actuator.deactuate(brew_state)
        else:
            return

    def _is_above_derivative_deadband(self, actual):
        return actual > (self.get_setpoint() + self._get_derivative_tripband_halfwidth())

    def _is_below_derivative_deadband(self, actual):
        return actual < (self.get_setpoint() - self._get_derivative_tripband_halfwidth())

    def _is_above_deadband(self, actual):
        return actual > (self.get_setpoint() + self._get_deadband_halfwidth())

    def _is_below_deadband(self, actual):
        return actual < (self.get_setpoint() - self._get_deadband_halfwidth())

    def _is_rising(self, actual):
        if self._last_state is None:
            return False
        else:
            return actual > self._get_last_actual() + self._derivative_threshold

    def _is_falling(self, actual):
        if self._last_state is None:
            return False
        else:
            return actual < self._get_last_actual() - self._derivative_threshold

    def _get_last_actual(self):
        return self.get_actual(self._last_state)

    def _is_in_upper_derivative_tripband(self, actual):
        s = self.get_setpoint()
        w = self._get_derivative_tripband_halfwidth()
        return s <= actual < s+w

    def _is_in_lower_derivative_tripband(self, actual):
        s = self.get_setpoint()
        w = self._get_derivative_tripband_halfwidth()
        return s-w <= actual < s

    def _is_in_deadband(self, actual):
        s = self.get_setpoint()
        w = self._get_deadband_halfwidth()
        return s-w <= actual < s+w

    def _get_derivative_tripband_halfwidth(self):
        return .5 * self._derivative_tripband_width

    def _get_deadband_halfwidth(self):
        return .5 * self._deadband_width

    def _raise_if_bandwidths_negative_or_derivative_band_too_large(self):
        if self._deadband_width < 0:
            raise RuntimeError("Deadband width must be positive")

        has_derivative_control = self._has_derivative_control()
        if has_derivative_control and self._derivative_tripband_width < 0:
            raise RuntimeError("Deriviative deadband width must be positive")

        if has_derivative_control and self._derivative_tripband_width >= self._deadband_width:
            raise RuntimeError("Derivative tripband must be smaller than deadband width")

        if self._derivative_threshold < 0:
            raise RuntimeError("Derivative threshold must be positive")

    def _has_derivative_control(self):
        has_derivative_control = self._derivative_tripband_width is not None
        return has_derivative_control


def extract_hlt_actual(brew_state):
    return brew_state.hlt_temperature


def extract_hex_actual(brew_state):
    return brew_state.hex_outlet_temperature