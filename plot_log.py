import argparse
from datetime import datetime
import numpy as N
import pylab as P
from scipy.signal import medfilt
parser = argparse.ArgumentParser(description='Plot the brewlog.')
parser.add_argument('file',  type=str, nargs=1,
                   help='Name of the logfile')

if __name__=="__main__":
    args = parser.parse_args()

    temperatures = []
    times = []
    with open(args.file[0], 'rb') as f:
        for line in f.readlines():
            xx = line.split(',')
            dt = xx[0]
            temps = map(float,xx[1:])
            try:
                dtime = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
            except:
                print dt
            times.append(dtime)
            temperatures.append(temps)

    temperatures = N.array(temperatures[:-1])
    t = [(dt-times[0]).total_seconds()/60.0 for dt in times[:-1]]
    P.plot(t, temperatures[:,0], 'k', label= 'HLT')
    P.plot(t, temperatures[:,1], 'g', label= 'Mash')
    P.plot(t, temperatures[:,2], 'r', label= 'Fermenter')
    P.xlabel('time, min')
    P.ylabel('temperature, C')
    P.legend(loc='upper left')
    P.show()
