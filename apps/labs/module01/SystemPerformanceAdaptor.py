'''
Created on Jan 17, 2019
Simple Python Application adaptor
@author: Shyama Sastha Krishnamoorthy Srinivasan
Fork for definitions from: https://github.com/Jahaja/psdash
'''

import psutil
import os
import platform
import socket
import time
from time import sleep
from threading import Thread

#initiating the class with a thread
class SystemPerformanceAdaptor(Thread):
    def __init__(self):
        Thread.__init__(self)
     
    #conditions to run the thread presented by the while loop and EnableAdaptor Flag    
    def run(self):
        while True:
            if self.EnableAdaptor:
                uptime = int(time.time() - psutil.boot_time())
                sysinfo = {
                    'uptime': uptime,
                    'hostname': socket.gethostname(),
                    'os': platform.platform(),
                    'load_avg': os.getloadavg(),
                    'num_cpus': psutil.cpu_count()
                    }
                #printing system information
                print(sysinfo)
                
                sm = psutil.swap_memory()
                swap = {
                    'total': sm.total,
                    'free': sm.free,
                    'used': sm.used,
                    'percent': sm.percent,
                    'swapped_in': sm.sin,
                    'swapped_out': sm.sout
                    }
                #printing memory change/swapping information
                print(swap)
                
                #printing cpu loads
                print('cpu times' + str(psutil.cpu_times_percent(0)._asdict()))
                
                #printing the number of cores in use
                print('cpu cores' + str([c._asdict() for c in psutil.cpu_times_percent(0, percpu=True)]))

                def get_disks(self, all_partitions=False):
                    disks = []
                    for dp in psutil.disk_partitions(all_partitions):
                        usage = psutil.disk_usage(dp.mountpoint)
                        disk = {
                            'device': dp.device,
                            'mountpoint': dp.mountpoint,
                            'type': dp.fstype,
                            'options': dp.opts,
                            'space_total': usage.total,
                            'space_used': usage.used,
                            'space_used_percent': usage.percent,
                            'space_free': usage.free
                            }
                        disks.append(disk)
                        #printing the available space for all the partitions
                        print(disks)
                #printing all the users logged in on the system        
                print('users' + str([u._asdict() for u in psutil.users()]))
            sleep(10)
            print("New update:")