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
    timeStamp = None
    name = 'Current Temperature'
    curValue = 0
    avgValue = 0
    minValue = 0
    maxValue = 0
    totValue = 0
    sampleCount = 0
    
    #takes in the current time as the time stamp
    def __init__(self):
        self.timeStamp = str(datetime.now())
    
    #function to add value to empty readings and increment values on consequent readings
    def addValue(self, newVal):
        self.sampleCount += 1
        self.timeStamp = str(datetime.now())
        self.curValue = newVal
        self.totValue += newVal
        if (self.curValue < self.minValue):
            self.minValue = self.curValue
        if (self.curValue > self.maxValue):
            self.maxValue = self.curValue
        if (self.totValue != 0 and self.sampleCount > 0):
            self.avgValue = self.totValue / self.sampleCount
    
    '''
    Various functions are listed below according to the requirements to retrieve information based
    on different levels of sensor output. i.e., for example the getAvgValue retrieves the average
    reading obtained to that point. each of the functions are self explanatory. 
    '''
    def getAvgValue(self):
        return self.avgValue
    
    def getMaxValue(self):
        return self.maxValue
    
    def getMinValue(self):
        return self.minValue
    
    def getValue(self):
        return self.curValue
    
    def setName(self, name):
        self.name = name
    
    #custom string output to print the obtained information          
    def __str__(self):
        customStr = \
            str(self.name + ':' + \
            os.linesep + '\tTime: ' + self.timeStamp + \
            os.linesep + '\tCurrent: ' + str(self.curValue) + \
            os.linesep + '\tAverage: ' + str(self.avgValue) + \
            os.linesep + '\tSamples: ' + str(self.sampleCount) + \
            os.linesep + '\tMin: ' + str(self.minValue) + \
            os.linesep + '\tMax: ' + str(self.maxValue))
            
        return customStr