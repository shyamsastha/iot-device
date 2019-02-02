'''
Created on Feb 1, 2019
Simple Python script to generate pseudo Actuator data
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import os
from datetime import datetime

COMMAND_OFF = 0 #To turn the actuator off
COMMAND_ON = 1 #To turn the actuator on
COMMAND_SET = 2 #To set value
COMMAND_RESET = 3 #To reset the value
STATUS_IDLE = 0 #To set the actuator state to idle
STATUS_ACTIVE = 1 #To set the actuator state to active

#Flags to check for errors

ERROR_OK = 0 
ERROR_COMMAND_FAILED = 1 #
ERROR_NON_RESPONSIBLE = -1

class ActuatorData():
    '''
    Initializing various values so it can be iterated in the functions below to produce
    variables that will be sent as Actuator information
    '''
    timeStamp = None
    name = 'Lights'
    hasError = False
    command = 0
    errCode = 0
    statusCode = 0
    stateData = None
    val = 0.0
    
    #initiates time stamp
    def __init__(self):
        self.updateTimeStamp()
    
    #Gets the command value
    def getCommand(self):
        return self.command
    
    #Gets the Name 
    def getName(self):
        return self.name

    #Gets the State of the device
    def getStateData(self):
        return self.stateDatae

    #Gets the status code of the device
    def getStatusCode(self):
        return self.statusCodee

    #Gets the error code if any
    def getErrorCode(self):
        return self.errorCode

    #Gets the vaule for the actuator        
    def getValue(self):
        return self.val;

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

    #Sets the Status code
    def setStatusCode(self, statusCode):
        self.statusCode = statusCode

    #Sets the error code
    def setErrorCode(self, errCode):
        self.errCode = errCode
        if (self.errCode != 0):
            self.hasError = True
        else:
            self.hasError = False
    
    #Sets the value for the actuator
    def setValue(self, val):
        self.val = val

    #Sends a data update for the actuator
    def updateData(self, data):
        self.command = data.getCommand()
        self.statusCode = data.getStatusCode()
        self.errCode = data.getErrorCode()
        self.stateData = data.getStateData()
        self.val = data.getValue()

    #Updates the time stamp for the time of actuation
    def updateTimeStamp(self):
        self.timeStamp = str(datetime.now())
    
    #Returns the Actuator data for display
    def __str__(self):
        customStr = \
            str(self.name + ':' + \
            os.linesep + '\tTime: ' + self.timeStamp + \
            os.linesep + '\tCommand: ' + str(self.command) + \
            os.linesep + '\tStatus Code: ' + str(self.statusCode) + \
            os.linesep + '\tError Code: ' + str(self.errCode) + \
            os.linesep + '\tState Data: ' + str(self.stateData) + \
            os.linesep + '\tValue: ' + str(self.val))
        return customStr