import brewControlClient as bcc
import time
from datetime import datetime
import os
import argparse

parser = argparse.ArgumentParser(description='Log the brew.')
parser.add_argument('file',  type=str, nargs=1,
                   help='Name of the logfile', 
                   default='erinstemp.log')

args = parser.parse_args()

def should_actuate(actual_temps, setpoint_temp):
    mean_temp = sum(actual_temps)/float(len(actual_temps))
    return (mean_temp-setpoint_temp)<-.5
    

builder = bcc.BrewCommandBuilder()
host = '192.168.11.101'
port = 8334
def get_client():
    return bcc.BrewControlClient(host, port)
    
def cook_temp_string(t):
    return float(t.replace('.-','.'))
    
def get_temps():
    client = get_client()
    client.sendMessage(builder.getMashActual())
    time.sleep(.1)
    rmsg = client.receiveMessages()
    mashActual = cook_temp_string(rmsg[0])
    client.close()
    
    client = get_client()
    client.sendMessage(builder.getHLTActual())
    time.sleep(.1)
    rmsg = client.receiveMessages()
    HLTActual = cook_temp_string(rmsg[0])
    client.close()
    
    client = get_client()
    client.sendMessage(builder.getFermenterActual())
    time.sleep(.1)
    rmsg = client.receiveMessages()
    fermenterActual = cook_temp_string(rmsg[0])
    client.close()
    
    return mashActual, HLTActual, fermenterActual
    
def log_temps(f, mashActual, HLTActual, fermenterActual):
    f.write(', '.join([str(datetime.now()), str(mashActual), str(HLTActual), str(fermenterActual)])+'\n')
    

if __name__=="__main__":
    host = '192.168.11.101'
    port = 8334
    
    testTemp = 30.0
    mashingTemp = 66.6
    strikeTemp = 74.0
    mashOutTemp = 76
    
    mashSetpoint = mashingTemp
    mashActual = 100
    
    cBuilder = bcc.BrewCommandBuilder()
    
    fpath = os.path.expanduser('~')
    fname = args.file[0]
    mash_prev = []
    with open(os.path.join(fpath, fname), 'a') as f:
        while True:
            print 'sensing...'
            
            mashActual, HLTActual, fermenterActual = get_temps()
            log_temps(f, mashActual, HLTActual, fermenterActual)
            
            print '    mash, HLT, Fermenter : %.1f, %.1f, %.1f'%(mashActual, HLTActual, fermenterActual)
            print ''
            
            mash_prev.insert(0,HLTActual)
            if len(mash_prev)>3:
                mash_prev.pop()

            if should_actuate(mash_prev, mashSetpoint):
                cmd = cBuilder.onMash()
            else:
                cmd = cBuilder.offMash()
                
            print 'taking control action...'
            print '    mash setpoint: %.1f'%mashSetpoint 
            client = get_client()
            print '    sending command: '+cmd
            client.sendMessage(cmd)
            time.sleep(.1)
            rmsg = client.receiveMessages()
            client.close()
            print ''
            time.sleep(1)
        
    
