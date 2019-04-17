'''
Created on April 12,2019
Simple Python script for AirQSensorAdaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from labbenchstudios.common.ConfigConst import UBIDOTS_CLOUD_SECTION,\
    CLOUD_API_KEY

'''
Imports to read from senseHAT, use JSON, use date and time for recording
Used to improve the existing temperature sensor adaptor application
''' 

from datetime import datetime
from ubidots import ApiClient
import json
from . import ConfigConst
from .ConfigUtil import ConfigUtil
from time import sleep
from threading import Thread
from .SensorData import SensorData
from .ActuatorData import ActuatorData
from .DataUtil import DataUtil
from .SmtpClientConnector import SmtpClientConnector
from .MqttClientConnector import MqttClientConnector

#Various command modes to be set on the actuator
COMMAND_AC = 0 #To turn on the air conditioner and turn off humidifier
COMMAND_HM = 1 #To turn on the humidifier and turn off air conditioner
COMMAND_RESET_AC = 2 #To set it back to air conditioner
COMMAND_RESET_HM = 3 #To set it back to humidifier

#Possible states of the actuator
STATUS_AC = 0 #To set the humidifier state to idle and turn on air conditioning
STATUS_HM = 1 #To set the humidifier state to active and turn off air conditioning

#Flags to check for errors
ERROR_OK = 0 
ERROR_COMMAND_FAILED = 1 
ERROR_NON_RESPONSIBLE = -1

config = ConfigUtil('../../../config/ConnectedDevicesConfig.props')
host = config.getProperty(ConfigConst.MQTT_GATEWAY_SECTION, ConfigConst.HOST_KEY)
api = ApiClient(token=config.getProperty(UBIDOTS_CLOUD_SECTION,CLOUD_API_KEY), base_url="http://yourcompanyname.api.ubidots.com/api/v1.6/")

class AirQSensorAdaptor(Thread):
    
    '''
    Initiating the thread for the Adaptor 
    creating the sensor data object and initial values to use inside Adaptor
    '''
    def __init__(self, name):
        Thread.__init__(self)
        self.enableAdaptor = True;
        self.sensorData = SensorData(name)
        self.actuator = ActuatorData("AC/Humidifier")
        self.connector = SmtpClientConnector()
        self.pubclient = MqttClientConnector();
        
    '''
    This thread gets the current temperature from SenseHat. 
    Notification is generated and mailed based on the threshold temperature set
    Signal is sent to actuator if nominal temperature doesn't match current value
    '''
    def run(self):
        while True:
            if self.enableAdaptor:
                data = DataUtil()
                json_data = data.sensorTojson(self.sensorData); #appends JSON data to file
                self.pubclient.publish(host,"airqm",json_data)
                #Print sensor information
                print('\n--------------------')
                print('New sensor readings:')
                print(' ' + str(self.sensorData))
                
                #checking for alerting difference and sending the message through SMTP
                if (int(self.sensorData.temperature)  >= 36):
                    print('\n Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Air conditioning is broken!!\n', json_data)
                elif (int(self.sensorData.humidity)  <= 34):
                    print('\n Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Humidifier needs a new filter!!\n', json_data)
                
                '''
                checking to see if the temperature exceeds nominal temperature to set status
                for actuator and send the message accordingly
                '''
                if(self.sensorData.temperature >= 35):
                    self.actuator.setCommand(COMMAND_AC)
                    self.actuator.setStatusCode(STATUS_AC)
                    self.actuator.setErrorCode(ERROR_OK)
                    self.actuator.setStateData('Air Conditioning ON')
                    print('\n Turning on Air COnditioning')
                    
                elif(self.sensorData.humidity <= 35):
                    self.actuator.setCommand(COMMAND_HM)
                    self.actuator.setStatusCode(STATUS_HM)
                    self.actuator.setErrorCode(ERROR_OK)
                    self.actuator.setStatusCode('Humidifier ON')
                    print('\n Turning on Air COnditioning')
                delay = int(config.getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.POLL_CYCLES_KEY))  
            sleep(delay)