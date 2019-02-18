'''
Created on Feb 17, 2019
Simple Python script to parse sensor data and actuator data to/from JSON files
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
import json
from labs.common.SensorData import SensorData
from labs.common.ActuatorData import ActuatorData

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
    def sensorTojson(self, SensorData):
        data = {};
        data['name'] = SensorData.name;
        data['avgVal'] = SensorData.avgVal;
        data['maxVal'] = SensorData.getMaxValue();
        data['minVal'] = SensorData.getMinValue();
        data['curVal'] = SensorData.getValue();
        data['time'] = str(SensorData.timestamp);
        self.jsonSd = json.dumps(data)
        outputSd = open('sensedata.txt','w')
        outputSd.write(self.jsonSd)
        return self.jsonSd
    
    '''
    Function to convert from Json type to sensor
    '''    
    def jsonTosensor(self,jsonData):
        sensedataDict = json.loads(jsonData)
        print(" decode [pre] --> " + str(sensedataDict))
        sensedata = SensorData()
        sensedata.name = sensedataDict['name']
        sensedata.timeStamp = sensedataDict['timeStamp']
        sensedata.avgValue = sensedataDict['avgValue']
        sensedata.minValue = sensedataDict['minValue']
        sensedata.maxValue = sensedataDict['maxValue']
        sensedata.curValue = sensedataDict['curValue']
        sensedata.totValue = sensedataDict['totValue']
        sensedata.sampleCount = sensedataDict['sampleCount']
        print(" decode [post] --> " + str(sensedata))
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
    def jsonToactuator(self,jsonData):
        actdataDict = json.loads(jsonData)
        print(" decode [pre] --> " + str(actdataDict))
        actdata = ActuatorData()
        actdata.name = actdataDict['name']
        actdata.timeStamp = actdataDict['timeStamp']
        actdata.hasError = actdataDict['hasError']
        actdata.command = actdataDict['command']
        actdata.errCode = actdataDict['errCode']
        actdata.statusCode = actdataDict['statusCode']
        actdata.stateData = actdataDict['stateData']
        actdata.curValue = actdataDict['curValue']
        print(" decode [post] --> " + str(actdata))
        return actdata