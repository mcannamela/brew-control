import unittest

from thermistor import Thermistor


class TestThermistor(unittest.TestCase):
    def setUp(self):
        self._analog_value = 511.5
        self._divider_resistance = 1e4
        self._exp_temperature = 298.15 - 273.15

        self._thermistor = Thermistor(self._divider_resistance)

    def test_get_temperature(self):
        self.assertAlmostEqual(self._thermistor.get_temperature(self._analog_value), self._exp_temperature)
        self.assertLess(self._thermistor.get_temperature(self._analog_value+1), self._exp_temperature)