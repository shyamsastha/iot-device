'''
Created on Jan 25, 2019
Simple Python script for Temp Sensor Adaptor - modified to accomodate JSON transactions
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

'''
Imports to read from senseHAT, use JSON, use date and time for recording
Used to improve the existing temperature sensor adaptor application
''' 

from datetime import datetime
from labs.common import DataUtil
import json
from labbenchstudios.common import ConfigUtil 
from labbenchstudios.common import ConfigConst

'''
Imports from the Initial temperature sensor adaptor application
'''
from random import uniform
from time import sleep
from threading import Thread
from labs.common import SensorData
from labs.common import ActuatorData
from labs.module02 import SmtpClientConnector
from labs.module03 import TempActuatorEmulator


class TempSensorAdaptor(Thread):
    
    #Setting initial values
    nominalTemp = 20
    
    '''
    Initiating the thread for the Adaptor 
    creating the sensor data object and initial values to use inside Adaptor
    '''
    def __init__(self, name):
        Thread.__init__(self)
        self.enableAdaptor = True;
        self.sensorData = SensorData.SensorData(name, 0, 30);
        self.actuator = ActuatorData.ActuatorData()
        self.connector = SmtpClientConnector.SmtpClientConnector()
        self.tempConf = ConfigUtil.ConfigUtil('../../../config/ConnectedDevicesConfig.props'); 
        self.actuatorEmulator = TempActuatorEmulator.TempActuatorEmulator();
    
    #function to dump json values into a file
    def fileWrite(self,value,filename):
        with open(filename,'w'):
            json.dumps(value)
        
    '''
    This thread gets the current temperature from SenseHat. 
    Notification is generated and mailed based on the threshold temperature set
    Signal is sent to actuator if nominal temperature doesn't match current value
    '''
    def run(self):
        while True:
            if self.enableAdaptor:
                #generate temperature information
                self.sensorData.curValue = uniform(float(self.sensorData.getMinValue()), float(self.sensorData.getMaxValue()))
                self.sensorData.addValue(self.sensorData.curValue)
                self.sensorData.diffVal = self.sensorData.curVal - self.sensorData.avgVal;
                print('\n--------------------')
                print('New sensor readings:')
                print(' ' + str(self.sensorData))
                
                #checking for alerting difference and sending the message through SMTP
                if (abs(self.sensorData.curVal >= (self.sensorData.getAvgValue() + 5))):               
                    data = DataUtil.DataUtil()
                    self.sensorData.timestamp = datetime.now().replace(microsecond=0);
                    json_data = data.sensorTojson(self.sensorData); #appends JSON data to file
                    #appends values to breach list in sensorData object
                    self.sensorData.breach_values.append(self.sensorData);
                    print(self.sensorData.breach_values)
                    print('\n Current tempConf exceeds average by > '
                          + str(self.sensorData.diffVal) + '. Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Exceptional sensor data!!\n', json_data) 
                
                '''
                checking to see if the temperature exceeds nominal temperature to set status
                for actuator and send the message accordingly
                '''
                if(self.sensorData.curVal > self.nominalTemp):
                   
                    self.actuator.setCommand(ActuatorData.COMMAND_ON)
                    self.actuator.setStatusCode(ActuatorData.STATUS_ACTIVE)
                    self.actuator.setErrorCode(ActuatorData.ERROR_OK)
                    self.actuator.setStateData('Decrease')
                    self.actuator.setValue(self.sensorData.curVal - self.nominalTemp)
                    self.actuatorEmulator.processMessage(self.actuator)
                    
                elif(self.sensorData.curVal < self.nominalTemp):
                
                    self.actuator.setCommand(ActuatorData.COMMAND_OFF)
                    self.actuator.setStatusCode(ActuatorData.STATUS_ACTIVE)
                    self.actuator.setErrorCode(ActuatorData.ERROR_OK)
                    self.actuator.setStatusCode('Increase')
                    self.actuator.setValue(self.sensorData.curVal - self.nominalTemp)
                    self.actuatorEmulator.processMessage(self.actuator)
                delay = int(self.tempConf.getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.POLL_CYCLES_KEY));     
            sleep(delay);