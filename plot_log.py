import argparse
from datetime import datetime
import numpy as N
import pylab as P
parser = argparse.ArgumentParser(description='Plot the brewlog.')
parser.add_argument('file',  type=str, nargs=1,
                   help='Name of the logfile')

args = parser.parse_args()

temperatures = []
times = []
with open(args.file[0], 'rb') as f:
    for line in f.readlines():
        dt,x = line.split(',')
        try:
            dtime = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
        except:
            print dt
        times.append(dtime)
        temperatures.append(x)

t = [(dt-times[0]).total_seconds()/60.0 for dt in times]
P.plot(t, temperatures, 'g')
P.xlabel('time, min')
P.ylabel('temperature, C')
P.show()
