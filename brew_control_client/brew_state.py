import datetime
import json
import pytz
from dateutil import parser

from brew_control_client.pin_config import PinConfig


class RawState(object):
    _DIGITAL_KEY = 'd'
    _ANALOG_KEY = 'a'
    _INTERRUPT_KEY = 'f_i'


    def __init__(self, state_as_json):
        self._state_as_json = state_as_json

    def get_digital_state(self):
        return list(map(bool,self._state_as_json[self._DIGITAL_KEY]))

    def get_analog_state(self):
        return self._state_as_json[self._ANALOG_KEY]

    def get_interrupt_state(self):
        return self._state_as_json[self._INTERRUPT_KEY]


class BrewState(object):
    TIME = 'TIME'
    HLT_TEMP = 'HLT_TEMP'
    HEX_OUTLET_TEMP = 'HEX_TEMP'
    HEX_INTERLOCK_TEMP = 'HEX_INTERLOCK_TEMP'
    FLOWRATE = 'PUMP_OUTLET_FLOWRATE'
    HLT_ACTUATED = 'HLT_ACTUATED'
    HEX_ACTUATED = 'HEX_ACTUATED'

    DATETIME_FORMAT = "%Y-%m-%d-%H:%M:%S.%f%z"

    @classmethod
    def build_from_json_str(cls, json_str):
        d = json.loads(json_str)
        return cls(
            float(d[cls.HLT_TEMP]),
            float(d[cls.HEX_OUTLET_TEMP]),
            float(d[cls.HEX_INTERLOCK_TEMP]),
            float(d[cls.FLOWRATE]),
            bool(d[cls.HLT_ACTUATED]),
            bool(d[cls.HEX_ACTUATED]),
            parser.parse(d[cls.TIME]),
        )

    def __init__(
            self,
            hlt_temperature,
            hex_outlet_temperature,
            hex_interlock_temperature,
            pump_outlet_flowrate,
            hlt_actuated,
            hex_actuated,
            dtime
    ):
        self.hlt_temperature = hlt_temperature
        self.hex_outlet_temperature = hex_outlet_temperature
        self.hex_interlock_temperature = hex_interlock_temperature
        self.pump_outlet_flowrate = pump_outlet_flowrate

        self.hlt_actuated = hlt_actuated
        self.hex_actuated = hex_actuated

        self.dtime = dtime

    def __repr__(self):
        s = '\n'.join([
            '{}: {}'.format(self.TIME, self.dtime.strftime(self.DATETIME_FORMAT)),
            '{}: {:.1f} C'.format(self.HLT_TEMP, self.hlt_temperature),
            '{}: {:.1f} C'.format(self.HEX_OUTLET_TEMP, self.hex_outlet_temperature),
            '{}: {:.1f} C'.format(self.HEX_INTERLOCK_TEMP, self.hex_interlock_temperature),
            '{}: {:.2f} L/min'.format(self.FLOWRATE, self.pump_outlet_flowrate*60.0),
            '{}: {}'.format(self.HLT_ACTUATED, self.hlt_actuated),
            '{}: {}'.format(self.HEX_ACTUATED, self.hex_actuated),
        ])

        return '<BrewState: {}>'.format(s)

    def render_to_json(self):
        return json.dumps({
            self.TIME: self.dtime.strftime(self.DATETIME_FORMAT),
            self.HLT_TEMP: self.hlt_temperature,
            self.HEX_OUTLET_TEMP: self.hex_outlet_temperature,
            self.HEX_INTERLOCK_TEMP: self.hex_interlock_temperature,
            self.FLOWRATE: self.pump_outlet_flowrate,
            self.HLT_ACTUATED: self.hlt_actuated,
            self.HEX_ACTUATED: self.hex_actuated})




class BrewStateFactory(object):
    def __init__(self, pin_config, thermistors_by_pin, flowrate_sensor):
        self._pin_config = pin_config
        self._thermistors_by_pin = thermistors_by_pin
        self._flowrate_sensor = flowrate_sensor

        assert isinstance(self._pin_config, PinConfig)

    def __call__(self, raw_state):
        return BrewState(
                self._get_hlt_temperature(raw_state),
                self._get_hex_outlet_temperature(raw_state),
                self._get_hex_interlock_temperature(raw_state),
                self._get_pump_outlet_flowrate(raw_state),
                self._get_hlt_actuated(raw_state),
                self._get_hex_actuated(raw_state),
                self._get_time()
        )

    def _get_hex_actuated(self, raw_state):
        return raw_state.get_digital_state()[self._pin_config.HEX_actuation_pin]

    def _get_hlt_actuated(self, raw_state):
        return raw_state.get_digital_state()[self._pin_config.HLT_actuation_pin]

    def _get_hex_interlock_temperature(self, raw_state):
        return self._get_temperature(raw_state, self._pin_config.HEX_interlock_thermistor_pin)

    def _get_hex_outlet_temperature(self, raw_state):
        return self._get_temperature(raw_state, self._pin_config.HEX_outlet_thermistor_pin)

    def _get_hlt_temperature(self, raw_state):
        return self._get_temperature(raw_state, self._pin_config.HLT_thermistor_pin)

    def _get_temperature(self, raw_state, pin_nr):
        thermistor = self._thermistors_by_pin[pin_nr]
        analog_value = raw_state.get_analog_state()[pin_nr]
        temperature = thermistor.get_temperature(analog_value)
        return temperature

    def _get_pump_outlet_flowrate(self, raw_state):
        pulse_frequency = raw_state.get_interrupt_state()[self._pin_config.flow_interrupt_pin_index]
        return self._flowrate_sensor.get_flowrate(pulse_frequency)

    def _get_time(self):
        return datetime.datetime.now(tz=pytz.utc)


class BrewStateProvider(object):

    def __init__(self, brew_state_factory, get_raw_state_fun):
        self._factory = brew_state_factory
        self._get_raw_state_fun = get_raw_state_fun

    def _get_raw_state(self):
        return self._get_raw_state_fun()

    def get_brew_state(self):
        return self._factory(self._get_raw_state())

