'''
Created on April 12,2019
Simple Python script for running the Air Quality Management Constrained Device Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from project.AirQSensorAdaptor import AirQSensorAdaptor
from time import sleep

#initiating the adaptor
airqsensorAdaptor = AirQSensorAdaptor("AirQuality")

#enabling the adaptor
airqsensorAdaptor.enableAdaptor = True

#starting the thread
airqsensorAdaptor.start()

#condition for the infinite loop
while (True):
    sleep(1)
    pass