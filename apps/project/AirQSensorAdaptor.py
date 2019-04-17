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

host = "127.0.0.1"

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
        
    '''
    This thread gets the current temperature from SenseHat. 
    Notification is generated and mailed based on the threshold temperature set
    Signal is sent to actuator if nominal temperature doesn't match current value
    '''
    def run(self):
        while True:
            if self.enableAdaptor:
                sleep(1)
                self.sensorData.updateValue()
                data = DataUtil()
                jsonData = data.sensorTojson(self.sensorData)
                #Print sensor information
                print('\n--------------------')
                print('New sensor readings for publishing:')
                print(' ' + str(self.sensorData))
                pubclient = MqttClientConnector()
                pubclient.publish(host,"airqm",jsonData)
            sleep(30)