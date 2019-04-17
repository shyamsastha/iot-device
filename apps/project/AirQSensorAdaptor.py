'''
Created on April 12,2019
Simple Python script for AirQSensorAdaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from . import ConfigConst
from .ConfigUtil import ConfigUtil
from time import sleep
from threading import Thread
from .SensorData import SensorData
from .ActuatorData import ActuatorData
from .DataUtil import DataUtil
from .SmtpClientConnector import SmtpClientConnector
from .MqttClientConnector import MqttClientConnector

config = ConfigUtil('ConnectedDevicesConfig.props')
host = config.getProperty(ConfigConst.MQTT_GATEWAY_SECTION, ConfigConst.HOST_KEY)

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
            sleep(30)