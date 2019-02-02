'''
Created on Feb 1, 2019
Simple Python script to activate LED on SenseHAT
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from time import sleep
import threading
import RPi.GPIO as GPIO #Using the RPi.GPIO proxy class

class SimpleLedActivator(threading.Thread):
    '''
    Initializing values to be used in the SimpleLED activation sequence
    Will be used if there are no values set by the actuator
    '''
    enableLed = False
    rateInSec = 1

    #Initializing self function
    def __init__(self, rateInSec = 1):
        super(SimpleLedActivator, self).__init__()
        
        if rateInSec > 0:
            self.rateInSec = rateInSec

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

    #Function to run the entire sequence
    def run(self):
        while True:
            if self.enableLed:
                GPIO.output(17, GPIO.HIGH)
                sleep(self.rateInSec)
                GPIO.output(17, GPIO.LOW)
                
            sleep(self.rateInSec)

    def getRateInSeconds(self):
        return self.rateInSec

    def setEnableLedFlag(self, enable):
        GPIO(17, GPIO.LOW)
        self.enableLed = enable