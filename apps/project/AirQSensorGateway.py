'''
Created on April 12,2019
Simple Python script for AirQSensorAdaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from time import sleep
from threading import Thread
from .SensorData import SensorData
from .ActuatorData import ActuatorData
from .DataUtil import DataUtil
from .SmtpClientConnector import SmtpClientConnector
from .MqttClientConnector import MqttClientConnector
from ubidots import ApiClient

#Various command modes to be set on the actuator
COMMAND_AC = 1 #To turn on the air conditioner and turn on the humidifier
COMMAND_HM = 2 #To turn on the air conditioner and turn off the humidifier 
COMMAND_RESET_AC = 3 #To turn off air conditioner and turn on the humidifier
COMMAND_RESET_HM = 4 #To turn off the air conditioner and turn off humidifier


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
controltoggle = api.get_variable('5cb791e4c03f977ab11854de')
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
                  
                '''
                Setting values to remote and getting values from remote to check for conditions
                '''
                tempremote.save_value({'value': self.sensorData.getTemperature()})
                pressremote.save_value({'value': self.sensorData.getPressure()})
                humidremote.save_value({'value': self.sensorData.getHumidity()})
                sleep(5)
                systemcheck = systemtoggle.get_values(1)
                controlcheck = controltoggle.get_values(1)
                
                '''
                checking to see if the temperature exceeds nominal temperature to set status
                for actuator and send the message accordingly
                '''
                if systemcheck[0]['value'] and controlcheck[0]['value']:
                    if systemcheck[0]['value'] == 1 and controlcheck[0]['value'] == 1:    
                        self.actuator.setCommand(COMMAND_AC)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStateData('Air Conditioning ON')
                        print('\n Air Conditioning and Humidifier ON')
                    elif systemcheck[0]['value'] == 1 and controlcheck[0]['value'] == 2:
                        self.actuator.setCommand(COMMAND_HM)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStateData('Air Conditioning OFF')
                        print('\n Air Conditioning ON. Turning OFF Humidifier')
                    if  systemcheck[0]['value'] == 2 and controlcheck[0]['value'] == 1:
                        self.actuator.setCommand(COMMAND_RESET_AC)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStateData('Humidifier ON')
                        print('\n Humidifier ON. Turning OFF Air Conditioning')
                    elif systemcheck[0]['value'] == 2 and controlcheck[0]['value'] == 2:
                        self.actuator.setCommand(COMMAND_RESET_HM)
                        self.actuator.setErrorCode(ERROR_OK)
                        self.actuator.setStateData('Humidifier OFF')
                        print('\n Turning OFF Air Conditioning and Humidifier')
                
                '''
                Checking for alerting difference and sending the message through SMTP
                '''
                if (self.sensorData.getTemperature()  >= 36):
                    print('\n Triggering alert...')
                    self.connector.publishMessage('Air conditioning is broken!!'
                    'Or maybe its just the thermostat... Check and get a new battery!\n', msg)
                elif (self.sensorData.getHumidity()  <= 34):
                    print('\n Triggering alert...')
                    self.connector.publishMessage('Humidifier needs a new filter!!'
                    'Or maybe stop wasting it needlessly :/\n', msg)        
            sleep(15)