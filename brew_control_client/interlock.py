class Interlock(object):

    def may_actuate(self, brew_state):
        return False

    def may_deactuate(self, brew_state):
        return True

class InterlockError(RuntimeError):
    pass


class HEXInterlock(Interlock):

    def __init__(self, flowrate_threshold, low_temp_threshold, high_temp_threshold):
        self._flowrate_threshold = flowrate_threshold
        self._low_temp_threshold = low_temp_threshold
        self._high_temp_threshold = high_temp_threshold

    def may_actuate(self, brew_state):
        return self._is_flowing(brew_state) and self._is_temperature_in_range(brew_state)

    def _is_flowing(self, brew_state):
        return brew_state.pump_outlet_flowrate >= self._flowrate_threshold

    def _is_temperature_in_range(self, brew_state):
        t = brew_state.hex_interlock_temperature
        return self._low_temp_threshold <= t <= self._high_temp_threshold





