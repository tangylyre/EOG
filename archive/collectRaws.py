from datetime import date
import time
import os
import numpy
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# from pygame import mixer  # Load the popular external library
# import pickle  # Rick
# import matplotlib.pyplot as plt
# from scipy import signal
# import scipy
from datetime import date

# BLUETOOTH PACKAGES I MAY NEED TO REMOVE
# sudo apt uninstall bluetooth pi-bluetooth bluez blueman

####################---Importing Data

###---This is for saving data
# with open('pattern.pkl','wb') as f:
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
f = open('josh.txt', 'a')
f.write("\n begin log for calibration v1")
f.write(str(date.today()))
x = 0
while True:
    c1 = chan1.voltage
    c2 = chan2.voltage
    s = ("\n%0.2f\t%0.2f" % (c1, c2))
    f.write(s)
    print(x, end=" ")
    time.sleep(0.05)
    x += 1
