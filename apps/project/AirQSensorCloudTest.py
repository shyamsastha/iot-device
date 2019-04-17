'''
Created on April 12,2019
Simple Python script for MQTT Subscriber Client
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''

import time
from ubidots import ApiClient
from project.SensorData import SensorData

TOKEN = "A1E-UectWsA40SKK5DI11B5C9yctwnwW0m"
api = ApiClient(token=TOKEN)
systemtoggle = api.get_variable('5cb671d3c03f9774a327220e')
tempremote = api.get_variable('5cb66e4dc03f9771f8685382')
pressremote = api.get_variable('5cb66e83c03f977258463fdc')
humidremote = api.get_variable('5cb66ea6c03f97729df16b3d')


def main():
    while True:
        time.sleep(5)
        sensorData = SensorData()
        sensorData.updateValue()
        tempremote.save_value({'value': sensorData.getTemperature()})
        pressremote.save_value({'value': sensorData.getPressure()})
        humidremote.save_value({'value': sensorData.getHumidity()})
        print("Data sent to cloud: \n" + str(sensorData))
        time.sleep(5)
        systemcheck = systemtoggle.get_values(1)
        print('systemcheck value: ' + str(systemcheck[0]['value']))
        if systemcheck[0]['value']:
            if systemcheck[0]['value'] == 1:
                print("System set to Humidifier")
            elif systemcheck[0]['value'] == 2:
                print("System set to Air Conditioner")
            elif systemcheck[0]['value'] == 3:
                print("Humidifier turned off")
            elif systemcheck[0]['value'] == 4:
                print("Air Conditioner turned off")

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)