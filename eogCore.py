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


def pullFourierProfile(t, Hz, eogChan):
    numFrames = t * Hz
    i = 0
    j = 0
    xf = fftfreq(numFrames, 1 / Hz)
    Y = []
    X = []
    t = 0
    while i < numFrames:
        X.append(t)
        t += 1 / Hz
        i += 1
        c1 = eogChan.voltage
        Y.append(c1)
        time.sleep(1 / Hz)
        currentTime = int(i) / int(Hz)
        print("seconds elapsed: %0.2f" % currentTime)
    yf = fourTransMag(Y)
    return [X, Y, xf, yf]


def subtractFourier(list1, list2):
    # runs through a numpy array and subtracts list 2 from list 1 element by element.
    # if the value is negative, just make it zero. This will make downstream of weighted frequencies.
    subtracted = list1
    if len(list1) == len(list2):
        i = 0
        for i in range(len(list1)):
            subtracted[i] = list1[i] - list2[i]
            if subtracted[i] < 0:
                subtracted[i] = 0
    return subtracted


def makeWeightProfile(eqFour):
    # accepts a normalized equalized profile, assigns each frequency a weight from 0 - 1 in relation to this numpy
    # array's maxima.
    weightedProfile = eqFour
    maxVal = np.amax(eqFour)
    for i in range(len(eqFour)):
        weightedProfile[i] = eqFour[i] / maxVal
    return weightedProfile


def weightedFreqMag(eqFour, weightedProfile):
    # accepts a fourier profile equalized against neutral dataset and a frequency set. generates a score weighing in
    # favor of the weighted profile
    score = 0
    i = 0
    for i in range(len(eqFour)):
        currentMag = eqFour[i]
        currentWeight = weightedProfile[i]
        score += currentMag * currentWeight
    return float(score)


def makeFourierThresholds(neuFour, disFour):
    # this function will accept the fourier profiles of neutral data and distress data, subtract them,
    # and generate a weighted criteria for distress.
    equalizedDistress = subtractFourier(disFour, neuFour)
    weightedProfile = makeWeightProfile(equalizedDistress)
    threshScore = weightedFreqMag(equalizedDistress, weightedProfile) * 0.75
    return weightedProfile, threshScore


def distressCheckFourier(currentFour, neutralProfile, weightedProfile, threshScore):
    eq = subtractFourier(currentFour, neutralProfile)
    score = weightedFreqMag(eq, weightedProfile)
    if score > threshScore:
        return True
    else:
        print("threshold not reached current value is "+str(score)+"\nrequires "+str(threshScore))
        return False


def calibrationV7Four(t, Hz, eogChan):
    print("Please look straight ahead for %d seconds. You will be signaled to stop." % t)
    time.sleep(5)
    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)
    print("Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to "
          "stop." % t)
    time.sleep(5)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan)
    time.sleep(1)
    print("done.")
    weightedProfile, threshScore = makeFourierThresholds(Yneu, Ydis)
    filename = input("input filename, or none for default\n")
    if len(filename) < 1:
        filename = "calibration_profile_%dHz_%dseconds.cali" % (Hz, t)
    else:
        filename = filename+'.cali'
    f = open(filename, 'w')
    currentTime = str(datetime.now()).replace(' ', '_')
    f.write('threshold score' + '\t' + str(threshScore) + '\t' + 'current time:\t' + currentTime + '\n')
    f.write("time(s)\tneutral(raw)\tdistress(raw)\tfrequency(Hz)\tneutral(mag)\tdistress(mag)\tweighted profile\n")
    for i in range(len(yfNeu)):
        line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\t' + str(xfDis[i]) + '\t' + str(
            yfNeu[i]) + '\t' + str(yfDis[i]) + '\t' + str(weightedProfile[i]) + '\n'
        f.write(line)
    f.close()
    return filename


def calibrationRead(filename):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        header = lines[0]
        threshScore = float(header.split('\t')[1])
        neutral = []
        weighted = []
        lines.pop(0)
        lines.pop(0)
        for i in range(len(lines)):
            line = lines[i].split('\t')
            neutral.append(float(line[4].replace('\n', '')))
            weighted.append(float(line[6].replace('\n', '')))
        return threshScore, neutral, weighted
    except FileNotFoundError:
        print("no file found under this filename.")
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
