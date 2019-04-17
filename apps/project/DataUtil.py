'''
Created on April 12,2019
Simple Python script to parse sensor data and actuator data to/from JSON files
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import json
from .SensorData import SensorData
from .ActuatorData import ActuatorData

'''
This class will help in parsing from and to JSON files
'''
class DataUtil(object):

    def __init__(self):
        '''
        Empty Constructor
        '''
    
    '''
    Function to convert from sensor to Json type
    '''
    def sensorTojson(self, sensorData):
        self.jsonSd = json.dumps(sensorData.__dict__)
        outputSd = open('sensedata.txt','w')
        outputSd.write(self.jsonSd)
        return self.jsonSd
    
    '''
    Function to convert from Json type to sensor
    '''    
    def jsonTosensor(self,jsonData):
        sensedataDict = json.loads(jsonData)
        sensedata = SensorData()
        sensedata.name = sensedataDict['name']
        sensedata.timeStamp = sensedataDict['timeStamp']
        sensedata.temperature = sensedataDict['temperature']
        sensedata.pressure = sensedataDict['pressure']
        sensedata.humidity = sensedataDict['humidity']
        return sensedata
    
    '''
    Function to convert from actuator to Json type
    '''
    def actuatorTojson(self,actdata):
        self.jsonAd = json.dumps(actdata.__dict__)
        outputAd = open('actdata.txt','w')
        outputAd.write(self.jsonAd)
        return self.jsonAd
    
    '''
    Function to convert from Json type to actuator
    '''    
    def jsonToactuator(self,jsonData, name):
        actdataDict = json.loads(jsonData)
        actdata = ActuatorData(name)
        actdata.name = actdataDict['name']
        actdata.time = actdataDict['timeStamp']
        actdata.hasError = actdataDict['hasError']
        actdata.command = actdataDict['command']
        actdata.errCode = actdataDict['errCode']
        actdata.statusCode = actdataDict['statusCode']
        actdata.stateData = actdataDict['stateData']
        return actdata