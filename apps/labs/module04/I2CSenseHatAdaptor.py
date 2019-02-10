'''
Created on Jan 26, 2019
Simple Python script for running the I2C Thread that reads from the SenseHAT module
@author: Shyama Sastha Krishnamoorthy Srinivasan
'''
import smbus
import threading
from time import sleep
from labs.common import ConfigUtil
from labs.common import ConfigConst

i2cBus = smbus.SMBus(1) # Uses I2C bus No.1 on Raspberry Pi3 +
#enableControl = 0x2D
#enableMeasure = 0x08
accelAddr = 0x1C # address for IMU (accelerometer)
magAddr = 0x6A # address for IMU (magnetometer)
pressAddr = 0x5C # address for pressure sensor
humidAddr = 0x5F # address for humidity sensor
begAddr = 0x28
totBytes = 5
DEFAULT_RATE_IN_SEC = 5

class I2CSenseHatAdaptor(threading.Thread):
    rateInSec = DEFAULT_RATE_IN_SEC
    def __init__(self):
        super(I2CSenseHatAdaptor, self).__init__()
        self.config = ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
        self.config.loadConfig()
        print('Configuration data...\n' + str(self.config))
        self.initI2CBus()
        
    def initI2CBus(self):
        print("Initializing I2C bus and enabling I2C addresses...")
        i2cBus.write_quick(accelAddr)
        i2cBus.write_quick(magAddr)
        i2cBus.write_quick(pressAddr)
        i2cBus.write_quick(humidAddr)
    '''
    Reading data from the adaptor and displaying them one by one
    '''
    #AccelerometerData
    def displayAccelerometerData(self):
        acceldata = i2cBus.read_i2c_block_data({accelAddr}, {begAddr}, {totBytes})
        print('Accelerometer Data points: \t' + str(acceldata))
        
    #MagnetometerData
    def displayMagnetometerData(self):
        magdata = i2cBus.read_i2c_block_data({magAddr}, {begAddr}, {totBytes})
        print('Magnetometer Data points: \t' + str(magdata))

    #PressureData
    def displayPressureData(self):
        pressdata = i2cBus.read_i2c_block_data({pressAddr}, {begAddr}, {totBytes})
        print('Pressure Data points: \t' + str(pressdata))
        
    #HumidityData
    def displayHumidityData(self):
        humiddata = i2cBus.read_i2c_block_data({humidAddr}, {begAddr}, {totBytes})
        print('Humidity Data points: \t' + str(humiddata))
            
    def run(self):
        while True:
            if self.enableEmulator:
                # Function calls to display various data on the screen
                self.displayAccelerometerData()
                self.displayMagnetometerData()
                self.displayPressureData()
                self.displayHumidityData()
            sleep(self.rateInSec)