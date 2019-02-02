'''
Created on Feb 1, 2019
Simple Python script to activate LED on SenseHAT
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from time import sleep
from sense_hat import SenseHat
import threading

class SenseHatLedActivator(threading.Thread):
    '''
    Initializing values to be used in the SensehatLED activation sequence
    Will be used if there are no values set by the actuator
    '''
    enableLed = False
    rateInSec = 1
    rotateDeg = 270
    sh = None
    displayMsg = None

    #Sets the activator to perform a specific sequence at a certain rate
    def __init__(self, rotateDeg = 270, rateInSec = 1):
        super(SenseHatLedActivator, self).__init__()
        
        if rateInSec > 0:
            self.rateInSec = rateInSec
        if rotateDeg >= 0:
            self.rotateDeg = rotateDeg
            
        self.sh = SenseHat()
        self.sh.set_rotation(self.rotateDeg)

    #Function to run the entire logic for switching LED on the senseHAT module 
    def run(self):
        while True:
            if self.enableLed:
                if self.displayMsg != None:
                    self.sh.show_message(str(self.displayMsg))
                else:
                    self.sh.show_letter(str('R'))
                
                sleep(self.rateInSec)
                self.sh.clear()
            sleep(self.rateInSec)

    #Function to get time cycle/ intervals
    def getRateInSeconds(self):
        return self.rateInSec

    #To set enabler flags
    def setEnableLedFlag(self, enable):
        self.sh.clear()
        self.enableLed = enable
    
    #To display message
    def setDisplayMessage(self, msg):
        self.displayMsg = msg