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
Hz = 500
Rf = 10
file = 'ArthurReadingFramev2.txt'

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P0)


# c1 = 0
# t = 0
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
    return X, Y, xf, yf, fig, ax, line


def main():
    hz = 500
    rf = 10
    X, Y, xf, yf, fig, ax, line = initPlot(rf, hz)
    f = open(file, 'w+')
    f.write("\n begin log for calibration v1")
    f.write(str(datetime.now()))
    q = False
    try:
        while not q:
            c1 = chan1.voltage
            Y[-1] = c1
            for x in range(len(Y) - 1):
                Y[x] = Y[x + 1]
            yf = fourTransMag(Y)
            line.set_ydata(yf)
            try:
                plt.draw()
                plt.pause(1 / Hz)
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
