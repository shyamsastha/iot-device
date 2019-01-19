'''
Created on Jan 17, 2019
Simple Python Application
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

from labs.module01 import SystemPerformanceAdaptor

#initiating the adaptor
sysPerfAdaptor = SystemPerformanceAdaptor.SystemPerformanceAdaptor()
#initiating the daemon
sysPerfAdaptor.daemon = True
print("Starting system performance app daemon thread...")
print("Update every 10 seconds...")
#enabling the adaptor
sysPerfAdaptor.EnableAdaptor = True
#starting the thread
sysPerfAdaptor.start()

#condition for the infinite loop
while (True):
    pass

if __name__ == '__main__':
    pass