'''
Created on Jan 25, 2019
Simple Python script to generate pseudo sensor data
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import os

from datetime import datetime
'''
This class creates the values required to randomize the data and generate pseudo data
which can be used a source for data collection that will be sent to the user through
the SmtpClientConnector
'''
class SensorData():
    '''
    Initializing various values to zero or null so it can be iterated in the functions below to produce
    variables that will be sent as sensor information
    '''
    timestamp = None
    name = 'Temperature'
    curVal = 0;
    avgVal = 0;
    minVal = 0;
    maxVal = 25;
    totVal = 0;
    diffVal = 0;
    sampleCount = 0;
    breach_values = list();
    
    #takes in the current time as the time stamp
    def __init__(self,name, minVal, maxVal):
        self.timestamp = str(datetime.now().replace(microsecond=0));
        self.name = name;
        self.maxVal = maxVal;
        self.minVal = minVal;
    
    #function to add value to empty readings and increment values on consequent readings
    def addValue(self, newVal):
        #self.sampleCount += 1
        self.timeStamp = str(datetime.now().replace(microsecond=0))
        self.curVal = newVal
        #self.totVal += newVal
        if (self.curVal < self.minVal):
            self.minVal = self.curVal
        if (self.curVal > self.maxVal):
            self.maxVal = self.curVal
        #if (self.totVal != 0 and self.sampleCount > 0):
            #self.avgVal = self.totVal / self.sampleCount
    
    '''
    Various functions are listed below according to the requirements to retrieve information based
    on different levels of sensor output. i.e., for example the getAvgValue retrieves the average
    reading obtained to that point. each of the functions are self explanatory. 
    '''
    def getAvgValue(self):
        return self.avgVal
    
    def getMaxValue(self):
        return self.maxVal
    
    def getMinValue(self):
        return self.minVal
    
    def getTotalValue(self):
        return self.totVal
    
    def getValue(self):
        return self.curVal
    
    def setName(self, name):
        self.name = name
    
    #custom string output to print the obtained information          
    def __str__(self):
        self.customStr = \
            str(self.name + ':' + \
            os.linesep + '\tTime: ' + self.timeStamp + \
            os.linesep + '\tCurrent: ' + str(self.curVal) + \
            os.linesep + '\tAverage: ' + str(self.avgVal) + \
            #os.linesep + '\tSamples: ' + str(self.sampleCount) + \
            os.linesep + '\tMin: ' + str(self.minVal) + \
            os.linesep + '\tMax: ' + str(self.maxVal))
            
        return self.customStr