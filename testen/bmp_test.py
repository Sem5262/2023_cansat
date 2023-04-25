from machine import Pin, I2C 
from bme280 import BME280, BMP280_I2CADDR

i2c = I2C(0,scl=Pin(9), sda=Pin(8)) # verander deze pinnen
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )

def height_from_pressure(pressure):
    """Calculate height in meters from pressure in pascals."""
    # Define constants
    g = 9.81    # gravitational acceleration in m/s^2
    M = 0.0289644    # molar mass of Earth's air in kg/mol
    R = 8.31447    # universal gas constant in J/(mol*K)
    T = 288.15    # standard temperature at sea level in K
    L = 0.0065    # temperature lapse rate in K/m
    p0 = 101325    # standard atmospheric pressure at sea level in Pa
    # Calculate altitude using the barometric formula
    height = (-1) * ((R * T) / (g * M * L)) * ((pressure / p0)**((g * M)/(R * L)) - 1)
    return height

while True:
    data = bmp.raw_values
    print(data) #temperatuur,druk,vochtigheid

    print(height_from_pressure(data[1]))