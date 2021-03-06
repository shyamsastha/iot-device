'''
Created on Jan 25, 2019
Simple Python script for running the Temp Management Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from labs.module03 import TempSensorAdaptor

#initiating the adaptor
tempSenseAdaptor = TempSensorAdaptor.TempSensorAdaptor()

#initiating the daemon
#tempSenseEmulator.daemon = True

#enabling the adaptor
tempSenseAdaptor.enableAdaptor = True

#starting the thread
tempSenseAdaptor.start()

#condition for the infinite loop
while (True):
    pass