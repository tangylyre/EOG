import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as animation
import time

import time
import busio
import digitalio
# import board
# import adafruit_mcp3xxx.mcp3008 as MCP
# from adafruit_mcp3xxx.analog_in import AnalogIn
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
# spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
# cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
# mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
# chan1 = AnalogIn(mcp, MCP.P0)
# chan2 = AnalogIn(mcp, MCP.P1)
f = open('josh.txt', 'a')
f.write("\n begin log for calibration v1")
f.write(str(date.today()))
x = 0
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
c1 = 0
t = 0
X = np.linspace(0, 10, 500)
Y = np.linspace(0, 0, 500)
graph = plt.plot(X, Y)[0]
plt.xlim([0, 10])
plt.ylim([0, 3.5])
while True:
    c1 += 0.001  # chan1.voltage
    Y[-1] = c1
    for x in range(len(Y) - 1):
        Y[x] = Y[x + 1]
    graph.set_ydata(Y)
    plt.draw()
    plt.pause(0.05)
