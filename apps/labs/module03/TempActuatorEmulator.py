'''
Created on Feb 1, 2019
Simple Python script for running the Temp Actuator Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from random import uniform
from time import sleep
from threading import Thread
from labs.common import ActuatorData
from labs.module02 import SmtpClientConnector

class TempActuatorEmulator(Thread):

    #creating the actuator data object and initial values to use inside Emulator
    actuatorData = ActuatorData.ActuatorData()
    connector = SmtpClientConnector.SmtpClientConnector()
    isPrevTempSet = False
    lowVal = 0
    highVal = 30
    alertDiff = 5
    
    #initiating the thread for the emulator
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            if self.enableEmulator:
                self.curTemp = uniform(float(self.lowVal), float(self.highVal))
                self.actuatorData.addValue(self.curTemp)
                print('\n--------------------')
                print('New Actuator readings:')
                print(' ' + str(self.actuatorData))
                
                if self.isPrevTempSet == False:
                    self.prevTemp = self.curTemp
                    self.isPrevTempSet = True
                else: 
                    if (abs(self.curTemp - self.actuatorData.getAvgValue()) >= self.alertDiff):
                        print('\n Current temp exceeds average by > ' + str(self.alertDiff) + '. Triggering alert...')
                        self.connector.publishMessage('Exceptional actuator data [test]', self.actuatorData)
            sleep(5)