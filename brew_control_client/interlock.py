class Interlock(object):

    def may_actuate(self, brew_state):
        return False

    def may_deactuate(self, brew_state):
        return True


class InterlockError(RuntimeError):
    pass


class FlowrateInterlock(Interlock):
    def __init__(self, flowrate_threshold):
        self._flowrate_threshold = flowrate_threshold

    def may_actuate(self, brew_state):
        return self._is_flowing(brew_state)

    def _is_flowing(self, brew_state):
        return brew_state.pump_outlet_flowrate >= self._flowrate_threshold


class TemperatureInterlock(Interlock):
    def __init__(self, low_fault_temp, high_fault_temp):
        self._low_fault_temp = low_fault_temp
        self._high_fault_temp = high_fault_temp

    def may_actuate(self, brew_state):
        return self._is_temperature_in_range(brew_state)

    def _is_temperature_in_range(self, brew_state):
        t = self._get_temperature(brew_state)
        return self._low_fault_temp <= t <= self._high_fault_temp

    def _get_temperature(self, brew_state):
        raise NotImplementedError()


class HEXOverheatingInterlock(TemperatureInterlock):
    def _get_temperature(self, brew_state):
        return brew_state.hex_interlock_temperature


class PumpCavitationInterlock(TemperatureInterlock):
    def _get_temperature(self, brew_state):
        return brew_state.hex_outlet_temperature


class HLTThermistorFaultInterlock(TemperatureInterlock):
    def _get_temperature(self, brew_state):
        return brew_state.hlt_temperature





