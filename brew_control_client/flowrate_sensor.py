class FlowrateSensor(object):
    def __init__(self, liters_per_pulse):
        self._liters_per_pulse = liters_per_pulse

    def get_flowrate(self, pulse_frequency):
        return pulse_frequency*self._liters_per_pulse
