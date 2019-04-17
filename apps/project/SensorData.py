'''
Created on April 12,2019
Simple Python script to generate sensor data
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import os
from datetime import datetime
from sense_hat import SenseHat
sense = SenseHat()

'''
This class creates the values required to randomize the data and generate pseudo data
which can be used a source for data collection that will be sent to the user through
the SmtpClientConnector
'''
class SensorData():
    '''
    Class variables
    '''
    timeStamp = str(datetime.now().replace(microsecond=0))
    name = "AirQm"
    temperature = round(sense.get_temperature(), 1)
    pressure = round(sense.get_pressure(), 1)
    humidity = round(sense.get_humidity(), 1)
    
    #takes in the current time as the time stamp
    def __init__(self, name = "AirQuality"):
        self.timestamp = str(datetime.now().replace(microsecond=0))
        self.name = name
        self.setTemperature()
        self.setPressure()
        self.setHumidity()
    
    #function to add value to empty readings and increment values on consequent readings
    def updateValue(self):
        self.temperature = round(sense.get_temperature(), 1)
        self.pressure = round(sense.get_pressure(), 1)
        self.humidity = round(sense.get_humidity(), 1)
        self.timeStamp = str(datetime.now().replace(microsecond=0))
    
    '''
    Various functions are listed below according to the requirements to retrieve information based
    on different levels of sensor output. i.e., for example the getAvgValue retrieves the average
    reading obtained to that point. each of the functions are self explanatory. 
    '''
    def getName(self):
        return self.name
            
    def getTemperature(self):
        return int(self.temperature)
    
    def getPressure(self):
        return int(self.pressure)
    
    def getHumidity(self):
        return int(self.humidity)
    
    def getTimestamp(self):
        return self.timeStamp

    def setName(self, name):
        self.name = name
        
    def setTemperature(self):
        self.temperature = sense.get_temperature()
    
    def setPressure(self):
        self.pressure = sense.get_pressure()
    
    def setHumidity(self):
        self.humidity = sense.get_humidity()
    
    def setTimestamp(self):
        self.timeStamp = str(datetime.now().replace(microsecond=0))
    
    #custom string output to print the obtained information          
    def __str__(self):
        return str(self.getName() + ':' + \
            os.linesep + '\tTime: ' + str(self.getTimestamp()) + \
            os.linesep + '\tTemperature: ' + str(self.getTemperature()) + \
            os.linesep + '\tPressure: ' + str(self.getPressure()) + \
            os.linesep + '\tHumidity: ' + str(self.getHumidity()))