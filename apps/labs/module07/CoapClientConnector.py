'''
Created on Mar 19, 2019

Simple Python script for Coap Client connector
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from coapthon.client.helperclient import HelperClient
from labs.common import ConfigConst
from labs.common.ConfigUtil import ConfigUtil
from labs.common.DataUtil import DataUtil
from labs.common.SensorData import SensorData
import os

client = None

class CoapClientConnector():
    config = None
    serverAddr = None
    host = "127.0.0.1"
    port = 5683
    
    def __init__(self):
        self.config = ConfigUtil('../../../config/ConnectedDevicesConfig.props')
        self.config.loadConfig()
        print('Configuration data...\n' + str(self.config)) 
        
        self.host = self.config.getProperty(ConfigConst.COAP_DEVICE_SECTION, ConfigConst.HOST_KEY)
        self.port = int(self.config.getProperty(ConfigConst.COAP_DEVICE_SECTION, ConfigConst.PORT_KEY))
        print('\tHost: ' + self.host)
        print('\tPort: ' + str(self.port))
        
        if not self.host or self.host.isspace():
            print("Using default host: " + self.host)
            
        self.serverAddr = (self.host, self.port)
        print('Server Address: ' + str(self.serverAddr))
        
        self.url = "coap://" + self.host + ":" + str(self.port) + "/Temperature"
    
    def initClient(self):
        try:
            self.client = HelperClient(server=(self.host, self.port))
            print("Coap Client created: " + str(self.client))
            print(" coap://" + self.host + ":" + str(self.port))
        except Exception:
            print("Failed to create CoAP helper client reference using host: " + self.host)
            pass
    
    def pingServer(self):
        self.initClient()
        cping = os.system("ping -c 1 " + self.host)
        if cping == 0 :
            print("Pinging Server...\n")
        else:
            print("Cannot ping Server!!\n")
        
    def responseHandler(self, response, resource):
        if response:
            print(response.pretty_print())
        else:
            print("No response received for GET using resource: " + resource)
        self.client.stop()
    
    def handleGet(self,resource):
        print("Testing GET for resource: " + str(resource))
        self.initClient()
        response = self.client.get(resource)
        self.responseHandler(response, resource)
    
    def handlePost(self, resource, payload):
        print("Testing POST for resource: " + resource + ", payload: " + payload)
        self.initClient()
        response = self.client.post(resource, payload)
        self.responseHandler(response, resource)
        
    def handlePut(self, resource, payload):
        print("Testing PUT for resource: " + resource + ", payload: " + payload)
        self.initClient()
        response = self.client.put(resource, payload)
        self.responseHandler(response, resource)

    def handleDelete(self, resource, payload):
        print("Testing delete for resource: " + resource + ", payload: " + payload)
        self.initClient()
        response = self.client.delete(resource, payload)
        self.responseHandler(response, resource)
        
    def runTests(self, resource):
        sensorData = SensorData(resource,10,30)
        sensorData.addValue(10)
        dataUtil = DataUtil()
        jsondata = dataUtil.sensorTojson(sensorData);
        self.initClient()
        self.pingServer()
        self.handleGet(resource)
        self.handlePost(resource, jsondata)
        self.handleGet(resource)
        sensorData.addValue(20)
        jsondata = dataUtil.sensorTojson(sensorData);
        self.handlePut(resource, jsondata)
        self.handleGet(resource)
        self.handleDelete(resource, jsondata)
        self.handleGet(resource)
     
if __name__ == '__main__':  # pragma: no cover
    pass