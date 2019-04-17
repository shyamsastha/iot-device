'''
Created on April 12,2019
Simple Python script to generate pseudo Actuator data
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import os
from datetime import datetime

class ActuatorData():
    '''
    Initializing various values so it can be iterated in the functions below to produce
    variables that will be sent as Actuator information
    '''
    name = None
    timeStamp = None
    hasError = False
    command = 0
    errorCode = 0
    stateData = None
    
    #initiates time stamp
    def __init__(self, name):
        self.updateTimeStamp()
        self.name = name
    
    #Gets the command value
    def getCommand(self):
        return self.command
    
    #Gets the Name 
    def getName(self):
        return self.name

    #Gets the State of the device
    def getStateData(self):
        return self.stateData

    #Gets the error code if any
    def getErrorCode(self):
        return self.errorCode

    #Checks for error
    def hasError(self):
        return self.hasError

    #Sets the command to run
    def setCommand(self, command):
        self.command = command

    #Sets the name of the actuator
    def setName(self, name):
        self.name = name

    #Sets the State data for the actuator
    def setStateData(self, stateData):
        self.stateData = stateData

    #Sets the error code
    def setErrorCode(self, errCode):
        self.errCode = errCode
        if (self.errCode != 0):
            self.hasError = True
        else:
            self.hasError = False

    #Sends a data update for the actuator
    def updateData(self, data):
        self.command = data.getCommand()
        self.errCode = data.getErrorCode()
        self.stateData = data.getStateData()

    #Updates the time stamp for the time of actuation
    def updateTimeStamp(self):
        self.timeStamp = str(datetime.now())
    
    #Returns the Actuator data for display
    def __str__(self):
        return str(self.name + ':' + \
            os.linesep + '\tTime: ' + self.timeStamp + \
            os.linesep + '\tCommand: ' + str(self.command) + \
            os.linesep + '\tError Code: ' + str(self.errCode) + \
            os.linesep + '\tState Data: ' + str(self.stateData))