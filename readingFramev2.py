import matplotlib.pyplot as plt
import numpy as np
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
# this is the same as readingframe v1 but with fourier implementation.
Hz = 500
Rf = 10
file = 'TylerReadingFramev2.txt'

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

f = open(file, 'a')
f.write("\n begin log for calibration v1")
f.write(str(datetime.now()))

q = False
while not q:
    c1 = chan1.voltage
    Y[-1] = c1
    for x in range(len(Y) - 1):
        Y[x] = Y[x + 1]
    graph.set_ydata(Y)
    plt.draw()
    plt.pause(1/Hz)
    f.write(str(c1)+'\n')
