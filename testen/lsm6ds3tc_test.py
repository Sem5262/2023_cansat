from machine import Pin, I2C 
from LSM6DS3TRC import LSM6DS3TRC
import time

i2c = I2C(0,scl=Pin(9), sda=Pin(8),freq=400000)# verander deze pins

lsm = LSM6DS3TRC(i2c)
 #hou stil bij calibratie op een platte oppervlakte

time.sleep(1)

while True:
    accel = lsm.get_accel_data()
    gyro = lsm.get_gyro_data()
    time.sleep(0.1)
    print(accel)