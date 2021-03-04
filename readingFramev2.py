import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
from fourierTrans import fourTransMag
import numpy as np
from numpy.fft import fftfreq
import matplotlib.pyplot as plt

# this is the same as readingframe v1 but with fourier implementation.

def initEOG():
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    # create an analog input channel on pin 0
    chanEOG = AnalogIn(mcp, MCP.P0)
    return chanEOG


def initVals(rf, Hz):
    X = np.linspace(0, rf, Hz)
    Y = np.linspace(0, 0, Hz)
    xf = fftfreq(len(Y), 1 / Hz)
    yf = fourTransMag(Y)
    return X, Y, xf, yf


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


def updatePlt(plt, line, yf):
    line.set_ydata(yf)
    plt.draw()
    plt.pause(1 / Hz)
    return


def popNdArray(new, ndArray):
    ndArray[-1] = new
    for x in range(len(ndArray) - 1):
        ndArray[x] = ndArray[x + 1]
    return ndArray


def main():
    try:
        file = str(input("Input the name of the file you'd like to write to:\n"))
        if file == '':
            file = 'rfDatav2.%s' % datetime.now()
    except ValueError:
        file = 'rfDatav2.%s' % datetime.now()
    hz = 500
    rf = 10
    X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz)
    f = open(file, 'w+')
    f.write("\n begin log for calibration v1")
    f.write(str(datetime.now()))
    q = False
    try:
        while not q:
            c1 = chan1.voltage
            Y = popNdArray(c1, Y)
            yf = fourTransMag(Y)
            try:
                updatePlt(plt, line, yf)
            except KeyboardInterrupt:
                plt.close()
                f.close()
                break
            f.write(str(c1) + '\n')
    except KeyboardInterrupt:
        plt.close()
        f.close()
    print("successfully quit.")


if __name__ == '__main__':
    main()
