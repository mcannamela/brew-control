import logging


class Interlock(object):

    def __init__(self, logger=None):
        self._fault_message = None
        self._logger = logger if logger is not None else logging.getLogger('interlock')

    def may_actuate(self, brew_state):
        return False

    def may_deactuate(self, brew_state):
        return True

    def _log_fault(self):
        self._logger.info("    FAULT {}: {}".format(self._fault_message, repr(self)))


class InterlockError(RuntimeError):
    pass


class FlowrateInterlock(Interlock):
    def __init__(self, low_flowrate_threshold, high_flowrate_threshold, logger=None):
        super(FlowrateInterlock, self).__init__(logger=logger)
        self._low_flowrate_threshold = low_flowrate_threshold
        self._high_flowrate_threshold = high_flowrate_threshold

    def __repr__(self):
        return "<{}: [{}, {}]>".format(self.__class__.__name__, self._low_flowrate_threshold, self._high_flowrate_threshold)

    def may_actuate(self, brew_state):
        may_actuate = self._is_flowing(brew_state)
        if not may_actuate:
            self._log_fault()
        return may_actuate

    def _is_flowing(self, brew_state):
        flowrate = brew_state.pump_outlet_flowrate
        if flowrate <= self._low_flowrate_threshold:
            self._fault_message = "FLOWRATE LOW"
        elif flowrate >= self._high_flowrate_threshold:
            self._fault_message = "FLOWRATE HIGH"
        return self._low_flowrate_threshold <= flowrate <= self._high_flowrate_threshold


class TemperatureInterlock(Interlock):
    def __init__(self, low_fault_temp, high_fault_temp, logger=None):
        self._low_fault_temp = low_fault_temp
        self._high_fault_temp = high_fault_temp
        super(TemperatureInterlock, self).__init__(logger=logger)

    def __repr__(self):
        return "<{}: [{}, {}]>".format(self.__class__.__name__, self._low_fault_temp, self._high_fault_temp)

    def may_actuate(self, brew_state):
        may_actuate = self._is_temperature_in_range(brew_state)
        if not may_actuate:
            self._log_fault()
        return may_actuate

    def _is_temperature_in_range(self, brew_state):
        t = self._get_temperature(brew_state)
        if t <= self._low_fault_temp:
            self._fault_message = "TEMPERATURE LOW"
        elif t >= self._high_fault_temp:
            self._fault_message = "TEMPERATURE HIGH"

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





