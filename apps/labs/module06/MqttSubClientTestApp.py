'''
Created on Mar 5, 2019
Simple Python script for MQTT Subscriber Client
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import logging
from labs.common import ConfigConst
from labs.common.ConfigUtil import ConfigUtil
from labs.common.DataUtil import DataUtil
from labs.module06.MqttClientConnector import MqttClientConnector

#Setting values for Topic and address for MQTT broker
topic = "Temperature Sensor"
config = ConfigUtil('../../../config/ConnectedDevicesConfig.props');
host = config.getProperty(ConfigConst.MQTT_GATEWAY_SECTION, ConfigConst.HOST_KEY)

subscribe = MqttClientConnector(topic)
subscribe.subscribe(host)                  # Connecting to MQTT Broker
msg = subscribe.message()                  # Subscribing to required topic
logging.debug('\nJSon Received: ')
print("\nReceived Json data: \n"+str(msg))

data = DataUtil();
sensorData = data.jsonTosensor(msg)        # Converting Jsondata to Sensordata
logging.debug('\nJson in "SensorData format": ')
print("\nMessage received in 'SensorData format': \n"+str(sensorData)+"\n")

jsondata = data.sensorTojson(sensorData)        # Converting Jsondata to Sensordata
logging.debug('\nBack to Json: ')
print("\nMessage converted back to Json: \n"+str(jsondata)+"\n")