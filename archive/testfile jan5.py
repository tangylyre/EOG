#Oculert V0.2
#Alexander Humen, Jeffrey Frese, Michael McCarney, and Mark Thibeault

####################---Import all relevant packages
import os
import numpy
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pygame import mixer  # Load the popular external library
import pickle # Rick
import matplotlib.pyplot as plt
from scipy import signal
import scipy

# BLUETOOTH PACKAGES I MAY NEED TO REMOVE
# sudo apt uninstall bluetooth pi-bluetooth bluez blueman

####################---Importing Data

###---This is for saving data
#with open('pattern.pkl','wb') as f:
#    pickle.dump([pattern, data],f)


####################---Reading the GPIO
    
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P0)
chan2 = AnalogIn(mcp, MCP.P1)


data = numpy.zeros(2000)
#data1 = numpy.zeros(2000)
#data2 = numpy.zeros(2000)
print('start')

t=time.time()

while true:
    print("1")
    print(chan1.voltage)
    print("2")
    print(chan2.voltage)
    time.sleep(0.5)