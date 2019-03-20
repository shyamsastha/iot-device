'''
Created on Mar 19, 2019

Simple Python script for Coap Server connector
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from coapthon.server.coap import CoAP
from labs.module07.TempResourceHandler import TempResourceHandler

from labbenchstudios.common.ConfigUtil import ConfigUtil
from labbenchstudios.common import ConfigConst

client = None

class CoapServerConnector(CoAP):

    def __init__(self):
        self.path = ""
        self.config = ConfigUtil('../../../config/ConnectedDevicesConfig.props')
        self.host = self.config.getProperty(ConfigConst.COAP_DEVICE_SECTION, ConfigConst.HOST_KEY)
        self.port = int(self.config.getProperty(ConfigConst.COAP_DEVICE_SECTION, ConfigConst.PORT_KEY))
        CoAP.__init__(self, (self.host, self.port))