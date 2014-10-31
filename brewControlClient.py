# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:03:49 2012

@author: Michael
"""
import socket
import time

class BrewControlClient(object):
    def __init__(self, host, port, bufferSize = 256):
        self.sock = socket.create_connection((host, port))
        self.bufferSize = bufferSize
        
    def sendMessage(self, msg):
        bytesExpectedToSend = len(msg)    
#        print "sending message: "+msg
        bytesSent = self.sock.send(msg)
        if bytesSent!=bytesExpectedToSend:
            raise MessageNotCompletedError("expected to sent %d bytes, did send %d"%(bytesSent,bytesExpectedToSend))
    
    def receiveMessages(self, timeout = 10):
        msgs = ''
        self.sock.settimeout(timeout)
        start = time.time()
        while True:
            s = self.sock.recv(self.bufferSize, )
            msgs+= s
            
            if msgs[-1]=='\n':
#                print "received message:"
#                print msgs
                
                break
            else:
                if (time.time()-start)>timeout:
                    raise TimeoutError('timed out waiting for newline')
#                print "waiting for server..."
                time.sleep(.005)
                
        return msgs[:-1].split('\n')
        
    def parseMessage(self, msg):
        var, val = msg.split(BrewCommandBuilder().reportSeparator)
        return (var, float(val))
    
    def close(self):
        self.sock.close()
        
class BrewCommandBuilder(object):
    def __init__(self):

        self.set = 'SET'
        self.get = 'GET'
        self.on  = 'ON'
        self.off = 'OFF'
        
        self.setpoint = 'SETPOINT'
        self.actual =   'ACTUAL'
        
        self.hlt =       'HLT'
        self.mash =      'MASH'
        self.fermenter = 'FERMENTER'
        
        self.temperatureUnits = 'C'
        
        self.commandSeparator = ':'
        self.variableSeparator = '_'
        self.argumentSeparator = '-'
        self.reportSeparator = '='
        
    def commandDict(self):
        commandNicks = [
                        'HLT on',
                        'mash on',
                        'fermenter on',
                        
                        'HLT off',
                        'mash off',
                        'fermenter off',
        
#                        'set HLT temp',
#                        'set mash temp',
#                        'set fermenter temp',
#                        
#                        'get HLT setpoint',
#                        'get mash setpoint',
#                        'get fermenter setpoint',
#
                        'get HLT actual',
                        'get mash actual',
                        'get fermenter actual'
                        ]
        commands = [
                    self.onHLT,        
                    self.onMash,        
                    self.onFermenter,        
                    
                    self.offHLT,        
                    self.offMash,        
                    self.offFermenter,        
        
#                    self.setHLT,
#                    self.setMash,
#                    self.setFermenter,
#                    
#                    self.getHLTSetpoint,
#                    self.getMashSetpoint,
#                    self.getFermenterSetpoint,
#                    
                    self.getHLTActual,
                    self.getMashActual,
                    self.getFermenterActual
                    ]
        return dict(zip(commandNicks, commands))
    
    def setCommand(self, varString):
        return self.set+self.commandSeparator+varString.strip()
    def getCommand(self, varString):
        return self.get+self.commandSeparator+varString.strip()
    def onCommand(self, varString):
        return self.on+self.commandSeparator+varString.strip()
    def offCommand(self, varString):
        return self.off+self.commandSeparator+varString.strip()
    
        
    def setHLT(self, T):
        assert type(T)==type(0.0)
        return self.setCommand(self.floatArgCombine(self.hltSetpoint(), T))
    def setMash(self, T):
        assert type(T)==type(0.0)        
        return self.setCommand(self.floatArgCombine(self.mashSetpoint(), T))
    def setFermenter(self, T):
        assert type(T)==type(0.0)
        return self.setCommand(self.floatArgCombine(self.fermenterSetpoint(), T))
        
    def onHLT(self):
        return self.onCommand(self.hlt)
    def onMash(self):
        return self.onCommand(self.mash)
    def onFermenter(self):
        return self.onCommand(self.fermenter)
    
    def offHLT(self):
        return self.offCommand(self.hlt)
    def offMash(self):
        return self.offCommand(self.mash)
    def offFermenter(self):
        return self.offCommand(self.fermenter)
        
    
    def getHLTSetpoint(self):
        return self.getCommand(self.hltSetpoint())
    def getMashSetpoint(self):
        return self.getCommand(self.mashSetpoint())
    def getFermenterSetpoint(self):
        return self.getCommand(self.fermenterSetpoint())   
        
    def getHLTActual(self):
        return self.getCommand(self.hltActual())
    def getMashActual(self):
        return self.getCommand(self.mashActual())
    def getFermenterActual(self):
        return self.getCommand(self.fermenterActual())  
    
    def varCombine(self, a, b):
        return a.strip()+self.variableSeparator+b.strip()
    def intArgCombine(self, cmd, theArg):
        return cmd.strip()+self.argumentSeparator+'%d'%theArg
    def floatArgCombine(self, cmd, theArg):
        return cmd.strip()+self.argumentSeparator+'%.1f'%theArg
        
    def hltActual(self):
        return self.hlt#self.varCombine(self.hlt, self.actual)
    def hltSetpoint(self):
        return self.varCombine(self.hlt, self.setpoint)
    def mashActual(self):
        return self.mash#self.varCombine(self.mash, self.actual)
    def mashSetpoint(self):
        return self.varCombine(self.mash, self.setpoint)
    def fermenterActual(self):
        return self.fermenter#self.varCombine(self.fermenter, self.actual)
    def fermenterSetpoint(self):
        return self.varCombine(self.fermenter, self.setpoint)
        
    
class MessageNotCompletedError(ValueError):
    pass
class TimeoutError(ValueError):
    pass

if __name__=="__main__":
    host = '192.168.11.101'
    port = 8334
    
    
    cDict = BrewCommandBuilder().commandDict()
    keys = cDict.keys()
    keys.sort()
    
    echoCount = 0
    
    try:
        while True:
            
            for i, cmd in enumerate(keys):
                print '%d. '%i+cmd+':'
            while True:
                selection = raw_input('choose a command: ')            
                try:
                    selectionInt = int(selection)
                    assert selectionInt>=0 and selectionInt<len(keys)
                    break
                except:
                    print "invalid choice"
                    pass
            command = keys[selectionInt]
            
            if command.split()[0]=='set':
                while True:
                    temperatureString = raw_input('enter the setpoint temperature: ')            
                    try:
                        T = float(temperatureString)
                        break
                    except:
                        print "invalid temperature"
                        pass
                message = cDict[command](T)
            else:
                message = cDict[command]()            
            
            client = BrewControlClient(host, port)
            client.sendMessage(message)
            time.sleep(.1)
            print "\nsent the message: "+message
            echoedMessages = client.receiveMessages()
            print "got the echo(s): "
            for E in echoedMessages:
                print E
            print ''
            time.sleep(.1)
            client.close()
            echoCount+=1;
            
    finally:
        print "made it through %d echoes"%echoCount
        client.close()
        
    
    
    
    