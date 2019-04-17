'''
Created on Mar 5, 2019

Simple Python script for MQTT Client connector
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

'''
Multiple imports for mqtt from the paho mqtt library
'''

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from asyncio.tasks import sleep
import time
import logging

class MqttClientConnector():
    host = "iot.eclipse.org"
    jsondata = "Hello"
    
    def on_connect(self,client,userdata,flags,rc):
        '''
        Function to execute once the client connects with MQTT Broker (Callback function)
        '''
        logging.info("Connected with Client: "+ str(rc + 1))
        client.subscribe(self.topic,2)
    
    def on_message(self,client,userdata,msg):
        '''
        Function to execute once the client receives message from MQTT Broker (Callback function)
        ''' 
        global jsondata
        jsondata = str(msg.payload.decode("utf-8"))
        client.loop_stop()
    
    def __init__(self,topic=None):
        '''
        Constructor
        @param topic: Topic of the message to be published or subscribed 
        ''' 
        self.topic = topic;
        
    def publish(self,host,topic,message):
        '''
        Function to publish the message
        @param topic: Topic of the message
        @param message: Message to be sent
        @param host: Address of MQTT broker   
        '''
        client = mqtt.Client();
        client.connect(host,1883)
        client.publish(topic,message)
        
    def subscribe(self,host):
        '''
        Function to subscribe to a topic
        @param host: Address of MQTT broker 
        '''
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(host,1883,60)
        client.loop_start()
        time.sleep(30)
    
    def message(self):
        '''
        Function to store the data received from MQTT Broker
        @return: Data received from MQTT Broker
        '''
        global jsondata
        return jsondata