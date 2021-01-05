#Oculert V0.2
#Alexander Humen, Jeffrey Frese, Michael McCarney, and Mark Thibeault

###################---Import all relevant packages

import os
import numpy
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pygame import mixer
import pickle # Rick
import matplotlib.pyplot as plt
from scipy import signal
import scipy

###################---Reading the GPIO
    
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

###################---Making the beep

mixer.init()
mixer.music.load('/home/pi/Desktop/beep.mp3')

###################---Recording the data for 10 seconds

data = numpy.zeros(2000)

print('start')

t=time.time()
for x in range(len(data)):
    time.sleep(0.0025)
    data[x] = chan.voltage
print('elapsed initial time: '+ str(time.time()-t))

data = data - 1.6 ### NEED TO DETERMINE AN APPROPRIATE NUMBER OTHER THAN 1.6... CURRENTLY HARD CODED

###################---This is for saving data

name=input('ENTER YOUR FILENAME: ')
with open(name+'.pkl','wb') as f:
    pickle.dump([pattern, data],f)    

###################---Recording the data indefinitely
mixer.music.play()


