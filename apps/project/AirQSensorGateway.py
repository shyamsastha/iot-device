'''
Created on April 12,2019
Simple Python script for AirQSensorAdaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import logging
from . import ConfigConst
from .ConfigUtil import ConfigUtil
from time import sleep
from threading import Thread
from .SensorData import SensorData
from .DataUtil import DataUtil
from .SmtpClientConnector import SmtpClientConnector
from .MqttClientConnector import MqttClientConnector
from ubidots import ApiClient

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

#Setting values for Topic and address for MQTT broker
topic = "airqm"
config = ConfigUtil('ConnectedDevicesConfig.props')
host = config.getProperty(ConfigConst.MQTT_GATEWAY_SECTION, ConfigConst.HOST_KEY)
api = ApiClient(token=config.getProperty(ConfigConst.UBIDOTS_CLOUD_SECTION,ConfigConst.CLOUD_API_KEY))
systemtoggle = api.get_variable('5cb671d3c03f9774a327220e')
tempremote = api.get_variable('5cb66e4dc03f9771f8685382')
pressremote = api.get_variable('5cb66e83c03f977258463fdc')
humidremote = api.get_variable('5cb66ea6c03f97729df16b3d')

class AirQSensorGateway(Thread):
    
    '''
    Initiating the thread for the Adaptor 
    creating the sensor data object and initial values to use inside Adaptor
    '''
    def __init__(self, name):
        Thread.__init__(self)
        self.enableAdaptor = True
        self.connector = SmtpClientConnector()
        self.subscribe = MqttClientConnector(topic)
        self.sensorData = SensorData()
        self.data = DataUtil()
        self.msg
        
    '''
    This thread gets the current temperature from SenseHat. 
    Notification is generated and mailed based on the threshold temperature set
    Signal is sent to actuator if nominal temperature doesn't match current value
    '''
    def run(self):
        while True:
            if self.enableAdaptor:
                sleep(10)
                self.subscribe.subscribe(host)
                #Print sensor information
                self.msg = self.subscribe.message()                  # Subscribing to required topic
                logging.debug('\nJSon Received: ')
                print("\nReceived Json data: \n"+str(self.msg))
                self.sensorData = self.data.jsonTosensor(self.msg)        # Converting Jsondata to Sensordata
                logging.debug('\nJson in "SensorData format": ')
                print("\nMessage received in 'SensorData format': \n"+str(self.sensorData)+"\n")
                
                #checking for alerting difference and sending the message through SMTP
                if (self.sensorData.getTemperature()  >= 36):
                    print('\n Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Air conditioning is broken!!\n', self.msg)
                elif (self.sensorData.getHumidity()  <= 34):
                    print('\n Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Humidifier needs a new filter!!\n', self.msg)
                '''
                Setting values to remote and getting values from remote to check for conditions
                '''
                tempremote.save_value({'value': self.sensorData.getTemperature()})
                pressremote.save_value({'value': self.sensorData.getPressure()})
                humidremote.save_value({'value': self.sensorData.getHumidity()})
                sleep(5)
                systemcheck = systemtoggle.get_values(1)
                '''
                checking to see if the temperature exceeds nominal temperature to set status
                for actuator and send the message accordingly
                '''
                if systemcheck[0]['value']:
                    if systemcheck[0]['value'] == 1:    
                        self.actuator.setCommand(COMMAND_AC)
                        self.actuator.setStatusCode(STATUS_AC)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStateData('Air Conditioning ON')
                        print('\n Turning on Air COnditioning')
                    elif systemcheck[0]['value'] == 2:
                        self.actuator.setCommand(COMMAND_HM)
                        self.actuator.setStatusCode(STATUS_HM)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStatusCode('Humidifier ON')
                        print('\n Turning on Humidifier')
                    elif systemcheck[0]['value'] == 3:
                        self.actuator.setCommand(COMMAND_RESET_AC)
                        self.actuator.setStatusCode(STATUS_HM)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStatusCode('Humidifier OFF')
                        print('\n Turning off Humidifier')
                    elif systemcheck[0]['value'] == 4:
                        self.actuator.setCommand(COMMAND_RESET_HM)
                        self.actuator.setStatusCode(STATUS_HM)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStatusCode('Air Conditioning OFF')
                        print('\n Turning off Air Conditioning')  
            sleep(10)