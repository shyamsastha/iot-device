'''
Created on April 12,2019
Simple Python script for running the Air Quality Management Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from project.AirQSensorAdaptor import AirQSensorAdaptor
from project.AirQSensorGateway import AirQSensorGateway
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
if __name__ == '__main__':
    while (True):
        sleep(1)
        pass