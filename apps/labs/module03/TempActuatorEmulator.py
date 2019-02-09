'''
Created on Feb 1, 2019
Simple Python script for running the Temp Actuator Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''


from labs.common import ActuatorData

class TempActuatorEmulator(object):

    #creating the actuator data object and initial values to use inside Emulator
    actuatorData = ActuatorData.ActuatorData()
    
    #Initiating the Emulator to start the actuation and process the message
    def processMessage(self, actuatorData):
        
        if(self.actuatorData != actuatorData):
            if(actuatorData.getValue() > 0):
                print('       \n Reduce the Temperature by:' + str(actuatorData.getValue()))
                
                self.actuatorData.updateData(actuatorData)
            elif(actuatorData.getValue() < 0):
                print('       \n Increase the Temperature by: ' + str(abs(actuatorData.getValue())))
                
                self.actuatorData.updateData(actuatorData)