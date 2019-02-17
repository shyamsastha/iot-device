'''
Created on Jan 25, 2019
Simple Python script for running the Temp Management Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from labs.module05 import TempSensorAdaptor
from time import sleep

#initiating the adaptor
tempSenseAdaptor = TempSensorAdaptor.TempSensorAdaptor("Temperature data")

#initiating the daemon
tempSenseAdaptor.daemon = True

#enabling the adaptor
tempSenseAdaptor.enableAdaptor = True

#starting the thread
tempSenseAdaptor.start()

#condition for the infinite loop
while (True):
    sleep(1)
    pass