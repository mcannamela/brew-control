
class PinConfig(object):

    flow_interrupt_pin = 2
    HLT_actuation_pin = 4
    HEX_actuation_pin = 5

    HLT_thermistor_pin = 0
    HEX_outlet_thermistor_pin = 1
    HEX_interlock_thermistor_pin = 2

THERMISTOR_RESISTANCES = {
    PinConfig.HLT_thermistor_pin: 1e4,
    PinConfig.HEX_outlet_thermistor_pin: 1e4,
    PinConfig.HEX_interlock_thermistor_pin: 1e4,
}

FLOWRATE_SENSOR_LITERS_PER_PULSE = 2.25e-3


