import brewControlClient as bcc
import time

if __name__=="__main__":
    host = '192.168.11.101'
    port = 8334
    
    testTemp = 30.0
    mashingTemp = 67.2
    strikeTemp = 75.8
    mashOutTemp = 76
    
    mashSetpoint = strikeTemp
    mashActual = 100
    
    cBuilder = bcc.BrewCommandBuilder()
    
    while True:
        print 'sensing...'
        client = bcc.BrewControlClient(host, port)
        print '    sending command: '+cBuilder.getMashActual()
        client.sendMessage(cBuilder.getMashActual())
        time.sleep(.1)
        rmsg = client.receiveMessages()
        mashActual = float(rmsg[0])
        print '    mash (actual, setpoint): %.1f, %.1f'%(mashActual, mashSetpoint)
        client.close()
        print ''
        
        if (mashActual-mashSetpoint<-.5):
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
        
    