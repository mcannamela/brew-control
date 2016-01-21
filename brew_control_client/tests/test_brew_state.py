import unittest

from brew_state import RawState, BrewState, BrewStateFactory
from flowrate_sensor import FlowrateSensor
from pin_config import PinConfig, THERMISTOR_RESISTANCES, FLOWRATE_SENSOR_LITERS_PER_PULSE
from thermistor import Thermistor


class TestRawState(unittest.TestCase):
    def setUp(self):
        self._digital_state = [True, False, True]
        self._analog_state = [1.2, 3.4]
        self._interrupt_state = [5.6, 7.8]
        self._json_state = {
            RawState._DIGITAL_KEY: self._digital_state,
            RawState._ANALOG_KEY: self._analog_state,
            RawState._INTERRUPT_KEY: self._interrupt_state
        }

        self._state = RawState(self._json_state)

    def test_get_digital_state(self):
        self.assertEqual(self._state.get_digital_state(), self._digital_state)

    def test_get_analog_state(self):
        self.assertEqual(self._state.get_analog_state(), self._analog_state)

    def test_get_interrupt_state(self):
        self.assertEqual(self._state.get_interrupt_state(), self._interrupt_state)


class TestBrewState(unittest.TestCase):
    def test___init__(self):
        BrewState(25.0, 26.0, 27.0, .01, True, False)


class TestBrewStateFactory(unittest.TestCase):

    def setUp(self):
        self._pin_config = PinConfig()

        thermistor_pins = {
            self._pin_config.HLT_thermistor_pin,
            self._pin_config.HEX_outlet_thermistor_pin,
            self._pin_config.HEX_interlock_thermistor_pin
        }
        self._thermistors_by_pin = {pin: Thermistor(THERMISTOR_RESISTANCES[pin]) for pin in thermistor_pins}
        self._flowrate_sensor = FlowrateSensor(FLOWRATE_SENSOR_LITERS_PER_PULSE)

        self._digital_state = []
        self._populate_digital_state()

        self._analog_state = []
        self._populate_analog_state()

        self._interrupt_state = []
        self._populate_interrupt_state()

        self._json_state = {
            RawState._DIGITAL_KEY: self._digital_state,
            RawState._ANALOG_KEY: self._analog_state,
            RawState._INTERRUPT_KEY: self._interrupt_state
        }

        self._raw_state = RawState(self._json_state)

        self._factory = BrewStateFactory(self._pin_config, self._thermistors_by_pin, self._flowrate_sensor)


    def test___call__(self):
        brew_state = self._factory(self._raw_state)
        self.fail()

    def _populate_interrupt_state(self):
        for i in range(2):
            if i == self._pin_config.flow_interrupt_pin:
                self._interrupt_state.append(2.0)
            else:
                self._analog_state.append(float('nan'))

    def _populate_analog_state(self):
        for i in range(5):
            if i == self._pin_config.HLT_thermistor_pin:
                self._analog_state.append(511.5)
            elif i == self._pin_config.HEX_outlet_thermistor_pin:
                self._analog_state.append(520.0)
            elif i == self._pin_config.HEX_interlock_thermistor_pin:
                self._analog_state.append(420.0)
            else:
                self._analog_state.append(float('nan'))

    def _populate_digital_state(self):
        for i in range(16):
            if i == self._pin_config.HEX_actuation_pin:
                self._digital_state.append(True)
            elif i == self._pin_config.HLT_actuation_pin:
                self._digital_state.append(False)
            else:
                self._digital_state.append('blah')
