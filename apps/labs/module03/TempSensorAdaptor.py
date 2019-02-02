'''
Created on Jan 25, 2019
Simple Python script for Temp Sensor Adaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from random import uniform
from time import sleep
from threading import Thread
from labs.common import SensorData
from labs.module02 import SmtpClientConnector

class TempSensorAdaptor(Thread):

    #creating the sensor data object and initial values to use inside Adaptor
    sensorData = SensorData.SensorData()
    connector = SmtpClientConnector.SmtpClientConnector()
    isPrevTempSet = False
    lowVal = 0
    highVal = 30
    alertDiff = 5
    
    #initiating the thread for the Adaptor
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            if self.enableAdaptor:
                self.curTemp = uniform(float(self.lowVal), float(self.highVal))
                self.sensorData.addValue(self.curTemp)
                print('\n--------------------')
                print('New sensor readings:')
                print(' ' + str(self.sensorData))
                
                if self.isPrevTempSet == False:
                    self.prevTemp = self.curTemp
                    self.isPrevTempSet = True
                else: 
                    if (abs(self.curTemp - self.sensorData.getAvgValue()) >= self.alertDiff):
                        print('\n Current temp exceeds average by > ' + str(self.alertDiff) + '. Triggering alert...')
                        self.connector.publishMessage('Exceptional sensor data [test]', self.sensorData)
            sleep(5)