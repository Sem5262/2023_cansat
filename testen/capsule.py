from machine import SPI, Pin
from rfm69 import RFM69
import time
from machine import I2C
from bme280 import BME280, BMP280_I2CADDR
from LSM6DS3TRC import LSM6DS3TRC
i2c = I2C(0)
#init sd-Card
"""
spi = SPI(1,sck=Pin(14), mosi=Pin(15), miso=Pin(12))
cs = Pin(13)
sd = sdcard.SDCard(spi, cs)
uos.mount(sd, '/sd')"""

#BMP init
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )

#LSM6DS3TRC init
lsm = LSM6DS3TRC(i2c)

#rfm69 init
FREQ           = 433.1
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 120 # ID of this node
BASESTATION_ID = 100 # ID of the node (base station) to be contacted

spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ


rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node    = NODE_ID # This instance is the node 120
rfm.ack_retries = 0 
rfm.ack_wait    = 0 
rfm.destination = BASESTATION_ID


print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )
print( 'BaseStation NODE:', BASESTATION_ID )

def to_string(*args):
    data = ""
    for i, x in enumerate(args):
        data += str(x)
        if i != len(args) - 1:
            data += ","
    return data

BUFFER_SIZE = 100 # number of lines to buffer before saving to file

# initialize buffer and counter
buffer = []
counter = 0

while True:
    
    #get values
    
    bmp280 = bmp.raw_values
    
    temperature_rfm = rfm.temperature
    
    temperature_bmp = bmp280[0]
    pressure = bmp280[1]
    humidity = bmp280[2]
    
    accel = lsm.get_accel_data()
    accel_x = accel[0]
    accel_y = accel[1]
    accel_z = accel[2]
    
    gyro = lsm.get_gyro_data()
    gyro_x = gyro[0]
    gyro_y = gyro[1]
    gyro_z = gyro[2]
    
    data = to_string(temperature_bmp, pressure, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
    
    # add data to buffer
    buffer.append(data)
    counter += 1
    
    # if buffer is full, save to file and reset counter
    """
    if counter == BUFFER_SIZE:
        with open('/sd/data.csv', 'a') as f:
            f.write('\n'.join(buffer) + '\n')
        buffer = []
        counter = 0"""
   
   
    rfm.send(bytes(to_string(temperature_bmp, pressure, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z) , "utf-8") )
    time.sleep(0.1)

