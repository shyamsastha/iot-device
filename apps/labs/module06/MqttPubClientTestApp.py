'''
Created on Mar 5, 2019

Simple Python script for MQTT Publisher Client
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from random import uniform
from datetime import datetime
import logging

from labs.common import ConfigConst
from labs.common.ConfigUtil import ConfigUtil
from labs.common.SensorData import SensorData
from labs.common.DataUtil import DataUtil
from labs.module06.MqttClientConnector import MqttClientConnector

topic = "Temperature Sensor"

config = ConfigUtil('../../../config/ConnectedDevicesConfig.props');
host = config.getProperty(ConfigConst.MQTT_GATEWAY_SECTION, ConfigConst.HOST_KEY)

#Creating Sensor Data
sensorData = SensorData(topic,10,30)
sensorData.curVal = uniform(float(sensorData.getMinValue()), float(sensorData.getMaxValue())); 
sensorData.addValue(sensorData.curVal);
sensorData.diffVal = sensorData.curVal - sensorData.avgVal;
sensorData.timestamp = datetime.now().replace(microsecond=0);
logging.info('\nSensorData for sending: ')
print("\n"+str(sensorData));


#Converting SensorData to json format
data = DataUtil()
jsondata = data.sensorTojson(sensorData);
logging.info('\nSensorData after Json conversion: ')
print("\nSensorData in Json Format for publishing: \n"+str(jsondata)+"\n")

pubclient = MqttClientConnector();

#Function call to publish the Json to the MQTT broker through MQTT ClientConnector 
pubclient.publish(host,topic,jsondata)