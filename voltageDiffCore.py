from datetime import datetime
from numpy.fft import fftfreq
import matplotlib.pyplot as plt
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as EOG
import adafruit_mcp4725 as DAC
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
from scipy.fft import fft
import board
import time
import pyttsx3
from eogCore import *
from fourierCore import *


def getVoltDif(V):
    # this function takes list V and compares them against the previous, making dif an n-1 length list.
    # the extrema of this list is used to generate calibration parameters.
    dif = []
    numPoints = len(V)
    for i in range(numPoints):
        current = V[i]
        if i > 0:
            dif.append(abs(current - prev))
        prev = current
    difMax = max(dif)
    difMin = min(dif)
    difMean = sum(dif) / (numPoints - 1)
    return difMax, difMin, difMean


def generateThreshold(neutralMax, distressMean, distressMax):
    thresh = distressMean
    while thresh < neutralMax + 0.1 and thresh < distressMax - 0.1:
        thresh += 0.01
    return thresh


def evaluateThreshold(difMean, difMax, thresh):
    # modify this formula dramatically if we're running with voltage differential
    evalNum = difMean * .75 + difMax * .25
    if evalNum > thresh:
        return True
    else:
        return False


def calibrationV6Diff(t, Hz, eogChan):
    print("Please look straight ahead for %d seconds. You will be signaled to stop." % t)
    time.sleep(5)
    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)
    print("Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to "
          "stop." % t)
    time.sleep(5)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)
    neuMax, neuMin, neuMean = getVoltDif(Yneu)
    disMax, disMin, disMean = getVoltDif(Ydis)
    thresh = generateThreshold(neuMax, disMean, disMax)
    query = input('Write to file? (y/n)\n')
    if query == 'y':
        query = input('File name?\n')
        if len(query) == 0:
            fn = 'defaultProfile.cali'
        else:
            fn = query + '.cali'
        f = open(fn, 'w')
        f.write(str(thresh))
        f.close()
    return thresh


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
