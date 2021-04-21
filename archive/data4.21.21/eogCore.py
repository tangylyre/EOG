import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as EOG
import adafruit_mcp4725 as DAC
from adafruit_mcp3xxx.analog_in import AnalogIn
import board


# This set of methods includes the core function of the EOG unit, as well as the breakout board.

def initDAC():
    # this function initializes connection with the breakout board,
    # and is used to control the vibration motor. through attributes of the dac object.
    # Initialize I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Initialize MCP4725.
    try:
        dac = DAC.MCP4725(i2c)
    except ValueError:
        dac = DAC.MCP4725(i2c, address=63)
    # this will serve as a file storing core functions necesary to operate the EOG.
    return dac


def setVoltsNorm(dac, x):
    # this is a helper function to manipulate the breakout board's output normalized from 0-1 with respect to maximum
    # output (theoretically 5v @ 50mA?) the dac object should be initialized prior, and x is a value from 0-1,
    # that will change the breakout board's output.
    if x > 1:
        x = 1
    elif x < 0:
        x = 0
    dac.normalized_value = x
    return


def initEOG():
    # this function returns the object chanEOG, which will be used to monitor the current EOG voltage through
    # "chanEOG.voltage"
    try:
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)
        # create the mcp object
        mcp = EOG.MCP3008(spi, cs)
        # create an analog input channel on pin 0
        chanEOG = AnalogIn(mcp, EOG.P0)
    except:
        print("EOG not recognized, please recheck breadboard configuration.")
        chanEOG = False
    return chanEOG
