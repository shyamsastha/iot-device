'''
Created on April 12,2019
Simple Python script for running the Air Quality Management Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from .AirQSensorAdaptor import AirQSensorAdaptor
from .AirQSensorGateway import AirQSensorGateway
from time import sleep

#initiating the adaptor
airqsensorAdaptor = AirQSensorAdaptor("AirQuality")
airqsensorGateway = AirQSensorGateway("AirQuality")

#enabling the adaptor
airqsensorAdaptor.enableAdaptor = True
airqsensorGateway.enableAdaptor = True

#starting the thread
airqsensorGateway.start()
airqsensorAdaptor.start()

#condition for the infinite loop
while (True):
    sleep(1)
    pass