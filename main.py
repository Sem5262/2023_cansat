import uos
import time
import random
from can import Can

buzzer_pin1 = machine.Pin(28, machine.Pin.OUT)
pwm = machine.PWM(buzzer_pin1)

def buzz(freq):
    
    pwm.freq(freq)
    pwm.duty_u16(50000)

can = Can()

BUFFER_SIZE = 50
buffer = []
counter = 0

can.rtc_start()

buz = False
buzzer = 0
while True:
    try:
        data = can.get_data()
    except:
        with open("log.txt", "a") as f:
            f.write("Get Data ERR\n")

    hour = data[0]
    minute = data[1]

    # Check if it's been 1 hour and 30 minutes since the last buzz
    if (hour >= 1 and minute >= 30) or buz == True:
        buz = True
        if buzzer == 1:
            buzz(2000)
            buzzer = 0
        else:
            buzz(200)
            buzzer = 1
        
    second = data[2]
    temperature_bmp = data[3]
    temperature_rfm = data[4]
    pressure = data[5]
    accel_x = data[6]
    accel_y = data[7]
    accel_z = data[8]
    gyro_x = data[9]
    gyro_y = data[10]
    gyro_z = data[11]
    
    can_data = can.to_string(hour,minute,second,temperature_bmp,temperature_rfm, pressure, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
    
    buffer.append(can_data)
    counter += 1
    
    if counter == BUFFER_SIZE:
        
        with open(can.current_file_name, 'a') as f:
            f.write('\n'.join(buffer) + '\n')
        
        buffer = []
        counter = 0
        
        can.get_current_file_size()        
        if can.current_file_size > 100000:
            can.current_file_name = f'/sd/{can.folder_name}/data_{hour:02d}-{minute:02d}-{second:02d}.csv'
        
    
    try:
        can.rfm.send(bytes(can.to_string(temperature_bmp, pressure, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z), "utf-8"))
    except:
        pass
