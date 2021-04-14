from numpy.fft import fftfreq
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import pyttsx3


# this set of methods includes relevant mathematical calculations, plots, and text to speech methods.

def initVals(rf, Hz):
    # this function returns the expected X, Y, and fourier frequencies.
    # these values will be purged as the reading frame is updated.
    X = np.linspace(0, rf, Hz)
    Y = np.linspace(0, 0, Hz)
    xf = fftfreq(len(Y), 1 / Hz)
    yf = fft(Y)
    yf = np.sqrt(yf.real ** 2 + yf.imag ** 2)
    return X, Y, xf, yf


def initPlot(rf, Hz, freqBounds=[0, 20], magBounds=[0, 100]):
    # this function initializes a fourier plot with respect to frequency of sampling and reading frame.
    # assumes the bounds of 0, 20 Hz and 0-100 magnitude.
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


def initPlotFour(xf, yf, freqBounds=[0, 30], magBounds=[0, 1000]):
    # this is identical to the previous method, but does not initialize x and y values.
    # saving both of these due to archival dependencies, but this method is mainly used in recent scripts.
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


def initVolPlot(rf, Hz, voltBounds=[0, 4]):
    # plot methods for voltage and time plots. would remove from methods but has some archived dependencies.
    # keeping this in for stability.
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


def updatePlt(plt, line, yf, Hz):
    # this helper function replaces the y values of a line object and then refreshes the plot.
    # this is the core of visualizing a reading frame; not necessary outside of bugfixing.
    line.set_ydata(yf)
    plt.draw()
    plt.pause(1 / Hz)
    return


def popNdArray(new, ndArray):
    # ndArrays do not have a inbuilt pop function that behaves like i like.
    # this function puts a new value at the start of the list and pushes every value one stack back
    # ie first in first out stacking.
    ndArray[-1] = new
    for x in range(len(ndArray) - 1):
        ndArray[x] = ndArray[x + 1]
    return ndArray


def initSpeechEngine():
    # this initializes the speech engine, modify the below parameters if the voice is too scary.
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)  # setting up new voice rate
    return engine


def speakString(s, engine):
    # this makes the engine speak the string input as s.
    engine.say(s)
    engine.runAndWait()
    engine.stop()
    return
