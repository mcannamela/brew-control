import math


class Thermistor(object):
    def __init__(self, divider_resistance):
        self._divider_resistance = divider_resistance

    def get_temperature(self, analog_value):
        thermistor_resistance = self._get_thermistor_resistance(analog_value)
        small = 1e-6
        thermistor_resistance = max(small, thermistor_resistance)
        inverse_temperature_kelvin = 1.0/298.15 + (1.0/3950.0)*math.log(thermistor_resistance/10000.0)
        temperature_centigrade = 1.0/inverse_temperature_kelvin - 273.15
        return temperature_centigrade

    def _get_thermistor_resistance(self, analog_value):
        try:
            thermistor_resistance = self._divider_resistance/(1023.0/(analog_value) -1)
        except ZeroDivisionError:
            return 1e12
        return thermistor_resistance

