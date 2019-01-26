'''
Created on Jan 25, 2019
Simple Python script for SMTP Client Connector
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from labs.common import ConfigUtil
from labs.common import ConfigConst
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
'''
Class to perform the SMTP client action between random data generator and the specified
email receiver on a regular cycle 
'''
class SmtpClientConnector(object):

    def __init__(self):
        self.config = ConfigUtil.ConfigUtil('../../../data/ConnectedDevicesConfig.props')
        self.config.loadConfig()
        print('Configuration data...\n' + str(self.config))
        
    #function to publish the message through the smtp headers   
    def publishMessage(self, topic, data):
        host = self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.HOST_KEY)
        port = self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.PORT_KEY)
        fromAddr = self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.FROM_ADDRESS_KEY)
        toAddr = self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.TO_ADDRESS_KEY)
        authToken = self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.USER_AUTH_TOKEN_KEY)
        
        msg = MIMEMultipart()
        msg['From'] = fromAddr 
        msg['To'] = toAddr
        msg['Subject'] = topic
        msgBody = str(data)
        
        msg.attach(MIMEText(msgBody))
        
        msgText = msg.as_string()

        # send e-mail notification
        smtpServer = smtplib.SMTP_SSL(host, port)
        smtpServer.ehlo()
        smtpServer.login(fromAddr, authToken)
        smtpServer.sendmail(fromAddr, toAddr, msgText)
        smtpServer.close()