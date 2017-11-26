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

from brew_control_client.brew_server import BrewServer
from brew_control_client.pin_command import CommandFactory
from brew_control_client.pin_config import THERMISTOR_BIASES_CENTIGRADE

parser = argparse.ArgumentParser(description='Brew.')
parser.add_argument('--logfile',
                    default='brew',
                    help='Name of the logfile and data file')

parser.add_argument('--append',
                    action='store_true',
                    help='If passed append to log and data files rather than start new.')

args = parser.parse_args()


def get_filename_stem():
    fpath = os.path.expanduser('~')
    fname = args.logfile
    return os.path.join(fpath, fname)


def get_log_filename():
    return get_filename_stem() + '.log'


def get_data_filename():
    return get_filename_stem() + '.json'


def get_client_factory():
    if args.append:
        mode = 'a'
    else:
        mode = 'w'
    logger = logging.getLogger('brew')
    logger.addHandler(logging.FileHandler(get_log_filename(), mode=mode))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    logger.info("Hello Brew!")

    pin_config = PinConfig()
    thermistors_by_pin = {
        pin: Thermistor(
            divider_resistance,
            bias_centigrade=THERMISTOR_BIASES_CENTIGRADE[pin]
        )
        for pin, divider_resistance in THERMISTOR_RESISTANCES.items()
    }
    flowrate_sensor = FlowrateSensor(FLOWRATE_SENSOR_LITERS_PER_PULSE)

    brew_state_factory = BrewStateFactory(pin_config, thermistors_by_pin, flowrate_sensor)
    brew_server = BrewServer()
    command_factory = CommandFactory(pin_config)

    client_factory = BrewControlClientFactory(command_factory,
                                              brew_state_factory,
                                              brew_server,
                                              logger=logger
                                              )

    return client_factory


if __name__ == "__main__":

    factory = get_client_factory()

    test_temp = 30.0
    mashing_temp = 65.20
    strike_temp = 80.0
    mash_out_temp = 78.0

    hlt_setpoint = strike_temp
    hex_setpoint = mashing_temp
    client = factory(
        hlt_setpoint,
        hex_setpoint,
        loop_delay_seconds=.5,
        hangover_delay_seconds=10
    )

    data_filename = get_data_filename()
    if not args.append:
        with open(data_filename, 'w') as f:
            f.write('')

    for brew_state in client:
        with open(data_filename, 'a') as f:
            f.write('\n')
            f.write(brew_state.render_to_json())
