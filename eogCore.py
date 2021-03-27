from numpy.fft import fftfreq
import matplotlib.pyplot as plt
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as EOG
import adafruit_mcp4725 as DAC
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
from scipy.fft import fft
import board


def initDAC():
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
    if x > 1:
        x = 1
    elif x < 0:
        x = 0
    dac.normalized_value = x
    return


def fourTransMag(y):
    yf = fft(y)
    mag = np.sqrt(yf.real ** 2 + yf.imag ** 2)
    return mag


def initEOG():
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
        chanEOG = False
    return chanEOG


def initVals(rf, Hz):
    X = np.linspace(0, rf, Hz)
    Y = np.linspace(0, 0, Hz)
    xf = fftfreq(len(Y), 1 / Hz)
    yf = fourTransMag(Y)
    return X, Y, xf, yf


def initVolPlot(rf, Hz, voltBounds=[0, 4]):
    timeBounds = [0, rf]
    X = np.linspace(0, rf, Hz)
    Y = np.linspace(0, 0, Hz)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Raw EOG Signal (Volts)')
    ax.set_xlabel('Time (s)')
    ax.set_title('Raw Voltage Monitor')
    line, = ax.plot(X, Y, 'b-')
    plt.xlim(timeBounds)
    plt.ylim(voltBounds)
    plt.grid()
    plt.ion()
    return X, Y, fig, plt, ax, line


def initPlot(rf, Hz, freqBounds=[0, 200], magBounds=[0, 100]):
    X, Y, xf, yf = initVals(rf, Hz)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Magnitude (Volts)')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_title('Fast Fourier Transform')
    line, = ax.plot(xf, yf, 'b-')
    plt.xlim(freqBounds)
    plt.ylim(magBounds)
    plt.grid()
    plt.ion()
    return X, Y, xf, yf, fig, plt, ax, line


def initPlotFour(xf, yf, freqBounds=[0, 200], magBounds=[0, 100]):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Magnitude (Volts)')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_title('Fast Fourier Transform')
    line, = ax.plot(xf, yf, 'b-')
    plt.xlim(freqBounds)
    plt.ylim(magBounds)
    plt.grid()
    plt.ion()
    return fig, plt, ax, line


def updatePlt(plt, line, yf, Hz):
    line.set_ydata(yf)
    plt.draw()
    plt.pause(1 / Hz)
    return


def popNdArray(new, ndArray):
    ndArray[-1] = new
    for x in range(len(ndArray) - 1):
        ndArray[x] = ndArray[x + 1]
    return ndArray
