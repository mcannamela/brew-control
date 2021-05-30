import unittest

from brew_control_client import FlowrateSensor


class TestFlowrateSensor(unittest.TestCase):
    def setUp(self):
        self._liters_per_pulse = 5.0
        self._pulse_frequency = 10.0
        self._exp_flowrate = 50.0

        self._flowrate_sensor = FlowrateSensor(self._liters_per_pulse)

    def test_get_flowrate(self):
        self.assertAlmostEqual(self._flowrate_sensor.get_flowrate(self._pulse_frequency), self._exp_flowrate)
