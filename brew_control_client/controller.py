class Controller(object):

    def __init__(self, actuator, extract_actual_fun):

        self._actuator = actuator
        self._extract_actual_fun = extract_actual_fun
        self._setpoint = None

    def control(self, brew_state):
        if self._should_actuate(brew_state):
            self._actuate(brew_state)
        else:
            self._handle_should_not_actuate(brew_state)

    def set_setpoint(self, setpoint):
        self._setpoint = setpoint

    def get_setpoint(self):
        return self._setpoint

    def get_actual(self, brew_state):
        self._extract_actual_fun(brew_state)

    def _actuate(self, brew_state):
        self._actuator.actuate(brew_state)

    def _should_actuate(self, brew_state):
        raise NotImplementedError()

    def _handle_should_not_actuate(self, brew_state):
        pass


class BangBangController(Controller):

    def __init__(self, actuator, extract_actual_fun, deadband_width):
        self._deadband_width = deadband_width

        super(BangBangController, self).__init__(actuator, extract_actual_fun)

    def _should_actuate(self, brew_state):
        return self.get_actual(brew_state) < self.get_setpoint() - self._deadband_width

    def _handle_should_not_actuate(self, brew_state):
        self._actuator.deactute(brew_state)
