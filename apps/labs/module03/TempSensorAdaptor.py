'''
Created on Jan 25, 2019
Simple Python script for Temp Sensor Adaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from random import uniform
from time import sleep
from threading import Thread
from labs.common import SensorData
from labs.common import ActuatorData
from labs.module02 import SmtpClientConnector
from labs.module03 import TempActuatorEmulator


class TempSensorAdaptor(Thread):

    #creating the sensor data object and initial values to use inside Adaptor
    sensorData = SensorData.SensorData()
    actuator = ActuatorData.ActuatorData()
    connector = SmtpClientConnector.SmtpClientConnector()
    actuatorEmulator = TempActuatorEmulator.TempActuatorEmulator()
    isPrevTempSet = False
    lowVal = 0
    highVal = 30
    nominalTemp = 20
    alertDiff = 5
    
    #initiating the thread for the Adaptor
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            if self.enableAdaptor:
                #generate temperature information
                self.curTemp = uniform(float(self.lowVal), float(self.highVal))
                self.sensorData.addValue(self.curTemp)
                print('\n--------------------')
                print('New sensor readings:')
                print(' ' + str(self.sensorData))
                
                if self.isPrevTempSet == False:
                    self.prevTemp = self.curTemp
                    self.isPrevTempSet = True
                else:
                    #checking for alerting difference and sending the message through SMTP
                    if (abs(self.curTemp - self.sensorData.getAvgValue()) >= self.alertDiff):
                        print('\n Current temp exceeds average by > ' + str(self.alertDiff) + '. Triggering alert...')
                        self.connector.publishMessage('Exceptional sensor data [test]', self.sensorData)
                
                '''
                checking to see if the temperature exceeds nominal temperature to set status
                for actuator and send the message accordingly
                '''
                if(self.curTemp > self.nominalTemp):
                   
                    self.actuator.setCommand(ActuatorData.COMMAND_ON)
                    self.actuator.setStatusCode(ActuatorData.STATUS_ACTIVE)
                    self.actuator.setErrorCode(ActuatorData.ERROR_OK)
                    self.actuator.setStateData('Decrease')
                    self.actuator.setValue(self.curTemp - self.nominalTemp)
                    self.actuatorEmulator.processMessage(self.actuator)
                    
                elif(self.curTemp < self.nominalTemp):
                
                    self.actuator.setCommand(ActuatorData.COMMAND_OFF)
                    self.actuator.setStatusCode(ActuatorData.STATUS_ACTIVE)
                    self.actuator.setErrorCode(ActuatorData.ERROR_OK)
                    self.actuator.setStatusCode('Increase')
                    self.actuator.setValue(self.curTemp - self.nominalTemp)
                    self.actuatorEmulator.processMessage(self.actuator)
            sleep(5)