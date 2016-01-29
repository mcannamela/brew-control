import argparse
from datetime import datetime
import numpy as np
import pylab as plb
from scipy.signal import medfilt

from brew_control_client.brew_state import BrewState

parser = argparse.ArgumentParser(description='Plot the brewlog.')
parser.add_argument('brewfile',  type=str, nargs=1,
                   help='Name of the brew')


if __name__=="__main__":
    args = parser.parse_args()

    data_filename = args.brewfile[0]

    brew_states = []

    with open(data_filename, 'rb') as f:
        for line in f.readlines()[1:]:
            try:
                brew_state = BrewState.build_from_json_str(line)
            except ValueError:
                raise
            else:
                brew_states.append(brew_state)

    temperatures = np.zeros((len(brew_states), 3))
    for i, s in enumerate(brew_states):
        temperatures[i] = np.array([s.hlt_temperature, s.hex_outlet_temperature, s.hex_interlock_temperature])
    flowrates = np.array([s.pump_outlet_flowrate for s in brew_states])

    max_temp = np.max(temperatures)
    hex_on = np.array([s.hex_actuated for s in brew_states])*.3*max_temp + .01*max_temp
    hlt_on = np.array([s.hlt_actuated for s in brew_states])*.25*max_temp + .005*max_temp

    dtimes = [s.dtime for s in brew_states]

    temperatures = np.array(temperatures)
    t = [(dt-dtimes[0]).total_seconds()/60.0 for dt in dtimes]
    plb.figure(figsize=(14, 9))
    plb.subplot(2,1,1)
    plb.plot(t, temperatures[:, 0], 'k', label='HLT')
    plb.plot(t, temperatures[:, 1], 'g', label='HEX Outlet')
    plb.plot(t, temperatures[:, 2], 'r', label='HEX Interlock')
    plb.plot(t, hex_on, 'm', label='HEX On')
    plb.plot(t, hlt_on, 'c', label='HLT On')

    plb.xlabel('time, min')
    plb.ylabel('temperature, C')
    plb.title('{}, t0={}'.format(data_filename, dtimes[0]))
    plb.legend(loc='upper left')

    plb.subplot(2,1,2)
    plb.plot(t, flowrates, 'k', label='Pump Outlet')
    plb.xlabel('time, min')
    plb.ylabel('flowrate, L/s')
    plb.title('{}, t0={}'.format(data_filename, dtimes[0]))
    plb.legend(loc='upper left')

    plb.show()
