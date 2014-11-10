import brewControlClient as bcc
import time
from datetime import datetime
import os

def should_actuate(actual_temps, setpoint_temp):
    mean_temp = sum(actual_temps)/float(len(actual_temps))
    return (mean_temp-setpoint_temp)<-.5

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
    fname = 'brewtemp.log'
    mash_prev = []
    with open(os.path.join(fpath, fname), 'a') as f:
        while True:
            print 'sensing...'
            client = bcc.BrewControlClient(host, port)
            print '    sending command: '+cBuilder.getMashActual()
            client.sendMessage(cBuilder.getMashActual())
            time.sleep(.1)
            rmsg = client.receiveMessages()
            mashActual = float(rmsg[0])
            f.write(', '.join([str(datetime.now()), str(mashActual)])+'\n')
            print '    mash (actual, setpoint): %.1f, %.1f'%(mashActual, mashSetpoint)
            client.close()
            print ''
            
            mash_prev.insert(0,mashActual)
            if len(mash_prev)>3:
                mash_prev.pop()
            print mash_prev

            if should_actuate(mash_prev, mashSetpoint):
                cmd = cBuilder.onMash()
            else:
                cmd = cBuilder.offMash()
                
            print 'taking control action...'
            client = bcc.BrewControlClient(host, port)
            print '    sending command: '+cmd
            client.sendMessage(cmd)
            time.sleep(.1)
            rmsg = client.receiveMessages()
            print '    recvd msg: '+rmsg[0]
            client.close()
            print ''
            time.sleep(10)
        
    
