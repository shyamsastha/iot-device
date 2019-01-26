'''
Created on Jan 25, 2019
Simple Python script for running the Temp Simulator Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from labs.module02 import TempSensorEmulator

#initiating the adaptor
tempSenseEmulator = TempSensorEmulator.TempSensorEmulator()
#initiating the daemon
tempSenseEmulator.daemon = True
#enabling the adaptor
tempSenseEmulator.EnableAdaptor = True
#starting the thread
tempSenseEmulator.start()

#condition for the infinite loop
while (True):
    pass

if __name__ == '__main__':
    pass