import numpy
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import scipy
from keyboard import is_pressed as key

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
# data1 = numpy.zeros(2000)
# data2 = numpy.zeros(2000)
print('start')

t = time.time()


def getMaxVol():
    q = False
    while not q:
        if key('q'):
            print("Stopping!")
            q = True