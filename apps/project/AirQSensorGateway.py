'''
Created on April 12,2019
Simple Python script for AirQSensorAdaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import logging
from time import sleep
from threading import Thread
from .SensorData import SensorData
from .ActuatorData import ActuatorData
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
TOKEN = "A1E-UectWsA40SKK5DI11B5C9yctwnwW0m"
host = "127.0.0.1"
api = ApiClient(token=TOKEN)
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
        self.sensorData = SensorData()
        self.actuator = ActuatorData("AC/Humidifier")
        self.data = DataUtil()
        
    '''
    This thread gets the current temperature from SenseHat. 
    Notification is generated and mailed based on the threshold temperature set
    Signal is sent to actuator if nominal temperature doesn't match current value
    '''
    def run(self):
        while True:
            if self.enableAdaptor:
                subclient = MqttClientConnector(topic)
                subclient.subscribe(host)
                #Print sensor information
                msg = subclient.message()                  # Subscribing to required topic
                print("\nReceived Json data: \n"+str(msg))
                self.sensorData = self.data.jsonTosensor(msg)        # Converting Jsondata to Sensordata
                
                #checking for alerting difference and sending the message through SMTP
                if (self.sensorData.getTemperature()  >= 36):
                    print('\n Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Air conditioning is broken!!\n', msg)
                elif (self.sensorData.getHumidity()  <= 34):
                    print('\n Triggering alert...')
                    #sends message through SMTP
                    self.connector.publishMessage('Humidifier needs a new filter!!\n', msg)
                '''
                Setting values to remote and getting values from remote to check for conditions
                '''
                tempremote.save_value({'value': self.sensorData.getTemperature()})
                pressremote.save_value({'value': self.sensorData.getPressure()})
                humidremote.save_value({'value': self.sensorData.getHumidity()})
                sleep(1)
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
            sleep(30)