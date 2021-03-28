import matplotlib.pyplot as plt
import numpy as np
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
from eogCore import *
Hz = 500
Rf = 10


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P0)

x = 0
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
c1 = 0
t = 0
X = np.linspace(0, Rf, Hz)
Y = np.linspace(0, 0, Hz)
graph = plt.plot(X, Y)[0]
plt.xlim([0, Rf])
plt.ylim([0, 3.5])
fi = "voltage_visualizer_datetime.now()"
currentTime = str(datetime.now()).replace(' ', '_')
try:
    file = str(input("Input the name of the file you'd like to write to:\n"))
    if file == '':
        file = 'FourierVis'
except ValueError:
    file = 'FourierVis'
file.replace(' ', '_')
f = open(file, 'w')
currentTime = str(datetime.now()).replace(' ', '_')
f.write(currentTime + '\n')
f.write("\n begin log for calibration v1")
f.write(file)

q = False
try:
    while not q:
        c1 = chan1.voltage
        Y[-1] = c1
        for x in range(len(Y) - 1):
            Y[x] = Y[x + 1]
        graph.set_ydata(Y)
        plt.draw()
        plt.pause(1/Hz)
        f.write(str(c1)+'\n')
except KeyboardInterrupt:
    f.close()
    pass
print("done!")
