import brewControlClient as bcc
import time
from datetime import datetime
import os
import argparse

parser = argparse.ArgumentParser(description='Plot the brewlog.')
parser.add_argument('--logfile',
                    default='brewtemp.log',
                    help='Name of the logfile')

args = parser.parse_args()

host = '192.168.11.101'
port = 8334
command_builder = bcc.BrewCommandBuilder()

MASH = 'mash'
HLT = 'hlt'
FERM = 'fermenter'

sense_commands = {MASH:command_builder.getMashActual(),
                HLT:command_builder.getHLTActual(),
                FERM:command_builder.getFermenterActual()}

on_commands = {MASH:command_builder.onMash(),
                  HLT:command_builder.onHLT(),
                  FERM:command_builder.onFermenter()}

off_commands = {MASH:command_builder.offMash(),
               HLT:command_builder.offHLT(),
               FERM:command_builder.offFermenter()}




def should_actuate(setpoint, actual):
    return (setpoint-actual)>.5 and actual<85.0

def get_client():
    return bcc.BrewControlClient(host, port)

def cook_temperature_string(t):
    return float(t.replace('.-','.'))

def get_temperature(command):
    client = get_client()
    client.sendMessage(command)
    time.sleep(.1)
    rmsg = client.receiveMessages()
    temperature = cook_temperature_string(rmsg[0])
    client.close()
    return temperature

def actuate(command):
    client = get_client()
    client.sendMessage(command)
    time.sleep(.1)
    rmsg = client.receiveMessages()
    print '    recvd msg: '+rmsg[0]
    client.close()

def get_temps():
    return {k:get_temperature(command) for k,command in sense_commands.items()}

def log_temps(f, temp_dict):
    keys = [HLT, MASH, FERM]
    x = map(str, [datetime.now()] + [temp_dict[k] for k in keys])
    s = ', '.join(x)
    print s
    f.write(s+'\n')

if __name__=="__main__":
    testTemp = 25.0
    mashingTemp = 66.6
    strikeTemp = 77.0
    mashOutTemp = 76.0
    
    #thermistor placed under outermost layer of insulation
    heater_safety_temp = 90.0
    
    
    mashSetpoint = strikeTemp
    hltSetpoint = mashOutTemp
    fermSetpoint = testTemp

    setpoints = {MASH:mashSetpoint,
                 HLT:hltSetpoint,
                 FERM:fermSetpoint}

    actuals = {MASH:100,
               HLT:100,
               FERM:100}

    fpath = os.path.expanduser('~')
    fname = args.logfile
    mash_prev = []
    with open(os.path.join(fpath, fname), 'a') as f:
        while True:
            print 'sensing...'
            actuals = get_temps()
            log_temps(f,actuals)

            print 'taking control action...'
            for k,t_actual in actuals.items():
                if actuals[FERM]>heater_safety_temp:
                    print '    unsafe heater temp detected, everything will be turned off!'                    
                    cmd = off_commands[k]
                else:    
                    if should_actuate(setpoints[k], t_actual) and k!=FERM:
                        cmd = on_commands[k]
                    else:
                        cmd = off_commands[k]

                print '    sending command: '+cmd
                actuate(cmd)

            time.sleep(2)
        
    
