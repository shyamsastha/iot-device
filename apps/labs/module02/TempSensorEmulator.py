'''
Created on Jan 25, 2019
Simple Python script for Temp Sensor Emulator
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from random import uniform
from time import sleep

class TempSensorEmulator(object):
    
    def run(self):
        while True:
            if self.enableEmulator:
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
            sleep(60)