import numpy
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import scipy
from keyboard import is_pressed as key
from keyboard import write
# this is an open source speech to text, lets see how it works.
import pyttsx3
from datetime import date


# create the spi bus
# spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
# cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
# mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
# chan1 = AnalogIn(mcp, MCP.P0)
# chan2 = AnalogIn(mcp, MCP.P1)

def getVol(x):
    # this function will get the voltage values of the last 30 seconds of recording, then determine the mean.
    # consider modifying algorithm with filter mechanisms if this result is inconsistent.
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    chan1 = AnalogIn(mcp, MCP.P0)
    # x is a value called in the main calibration function: 0 = middle prompt, 1 = upward prompt, -1 = downward prompt
    if x == 0:
        print("Please look directly ahead for at least 30 seconds and press Q when finished.")
    elif x > 0:
        print("Please look upwards without moving your neck for at least 30 seconds and press Q when finished.")
    elif x < 0:
        print("Please look downwards without moving your neck for at least 30 seconds and press Q when finished.")
    else:
        exit(-1)
    data = []
    q = False
    while not q:
        if key('q'):
            write('\n')
            print("Stopping!")
            q = True
        if len(data) > 30:
            data.pop(0)
            data.append(chan1.voltage)
        else:
            data.append(chan1.voltage)
        time.sleep(1)
    return sum(data) / len(data)


def getVolTimed(Hz, t, x):
    pause = 5
    # pause is an integer value that informs how long will the program will pause before reading input.
    engine = pyttsx3.init()
    # this function is the same as above but doesn't require keyboard input. instead it will wait 30 seconds and record
    # 30 seconds of input.
    # consider modifying algorithm with filter mechanisms if this result is inconsistent.
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    chan1 = AnalogIn(mcp, MCP.P0)
    # replace this chan definition when implementing on the pi
    # x is a value called in the main calibration function: 0 = middle prompt, 1 = upward prompt, -1 = downward prompt
    if x == 0:
        msg = "In "+str(pause)+" seconds, please look directly ahead for " + str(t) + " seconds."

    elif x > 0:
        msg = "In "+str(pause)+" seconds, please look upwards without moving your neck for " + str(t) + " seconds."

    elif x < 0:
        msg = "In "+str(pause)+" seconds, look downwards without moving your neck for " + str(t) + " seconds."
        # in case you are wondering, i string formatted this weird to make the text to speech work properly.
    else:
        exit(-1)
    print(msg)
    engine.say(msg)
    engine.runAndWait()
    data = []
    time.sleep(pause)
    i = 0
    print("starting...")
    engine.say("starting")
    engine.runAndWait()
    while i < t+1:
        print(i, end=" ")
        engine.say(str(i))
        engine.runAndWait()
        chan1 += 1
        data.append(chan1.voltage)
        time.sleep(1/Hz)
        i += 1
    print("\n")
    engine.stop()
    f = open("diagnostic.txt", "w+")
    f.write("\n begin log for calibration v1")
    f.write(str(date.today()))
    f.write("x = %d", x)
    for x in len(data):
        f.write(data(x))
    return sum(data) / len(data)


def calibrate(Hz, t):
    # Hz sets the refresh rate for the calibration. Consider reducing this to improve performance.
    # t sets the period of each calibration sampling. Reduce this for convenience sake, but increase if datapoints
    # are inconsistent.
    critical = []
    x = -1
    while x < 2:
        critical.append(getVolTimed(Hz, t, x))
        x += 1
    return critical

