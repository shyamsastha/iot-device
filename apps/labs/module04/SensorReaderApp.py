'''
Created on Jan 25, 2019
Simple Python script for running the Temp Management Application
modified to run as Sensor Reader app
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from labs.module04 import I2CSenseHatAdaptor

#initiating the adaptor
senseHatAdaptor = I2CSenseHatAdaptor.I2CSenseHatAdaptor()

#initiating the daemon
#tempSenseEmulator.daemon = True

#enabling the adaptor
senseHatAdaptor.enableEmulator = True

#starting the thread
senseHatAdaptor.start()

#condition for the infinite loop
while (True):
    pass