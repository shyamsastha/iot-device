'''
Created on Mar 19, 2019

Simple Python script for Coap Test Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
from labs.module07.CoapClientConnector import CoapClientConnector

#Initiating a client object and running the tests
_coapClient = CoapClientConnector()
_coapClient.runTests("Temperature");