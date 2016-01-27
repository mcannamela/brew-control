import logging

import sys

from brew_control_client import (BrewControlClientFactory,
                                 THERMISTOR_RESISTANCES,
                                 PinConfig,
                                 FLOWRATE_SENSOR_LITERS_PER_PULSE,
                                 FlowrateSensor,
                                 Thermistor,
                                 get_raw_state,
                                 get_index_response,
                                 BrewStateProvider,
                                 BrewStateFactory,
                                 issue_commands)
import os
import argparse


parser = argparse.ArgumentParser(description='Plot the brewlog.')
parser.add_argument('--logfile',
                    default='brewtemp.log',
                    help='Name of the logfile')

args = parser.parse_args()

def get_filename():
    fpath = os.path.expanduser('~')
    fname = args.logfile
    return os.path.join(fpath, fname)

def get_client_factory():
    logger = logging.getLogger('brew')
    logger.addHandler(logging.FileHandler(get_filename()))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    logger.info("Hello Brew!")

    pin_config = PinConfig()
    thermistors_by_pin = {pin: Thermistor(divider_resistance)
                          for pin, divider_resistance in THERMISTOR_RESISTANCES.items()
                          }
    flowrate_sensor = FlowrateSensor(FLOWRATE_SENSOR_LITERS_PER_PULSE)

    brew_state_factory = BrewStateFactory(pin_config, thermistors_by_pin, flowrate_sensor)
    get_brew_state = BrewStateProvider(brew_state_factory, get_raw_state).get_brew_state

    client_factory = BrewControlClientFactory(pin_config,
                             issue_commands,
                             get_brew_state,
                             logger=logger
                             )

    return client_factory

if __name__=="__main__":


    factory = get_client_factory()

    test_temp = 60.0
    mashing_temp = 66.6
    strike_temp = 80.0
    mash_out_temp = 78.0

    hlt_setpoint = test_temp
    hex_setpoint = test_temp
    client = factory(hlt_setpoint, hex_setpoint, loop_delay_seconds=2)

    client.run()