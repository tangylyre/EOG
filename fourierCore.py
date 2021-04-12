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
from eogCore import *
import pyttsx3
from utilitiesCore import *


def fourTransMag(y):
    yf = fft(y)
    mag = np.sqrt(yf.real ** 2 + yf.imag ** 2)
    return mag


def pullFourierProfile(t, Hz, eogChan, voiceEngine, speech):
    halfwayFlag = True
    numFrames = t * Hz
    i = 0
    xf = fftfreq(numFrames, 1 / Hz)
    Y = []
    X = []
    t = 0
    if speech:
        speakString("Beginning Test..", voiceEngine)
    while i < numFrames:
        X.append(t)
        t += 1 / Hz
        i += 1
        c1 = eogChan.voltage
        Y.append(c1)
        time.sleep(1 / Hz)
        currentTime = int(i) / int(Hz)
        print("seconds elapsed: %0.2f" % currentTime)
        if i >= numFrames / 2 and halfwayFlag:
            s = "%d seconds remain." % currentTime
            if speech:
                speakString(s, voiceEngine)
            halfwayFlag = False
    if speech:
        speakString("Finished.", voiceEngine)
    Yunfiltered = Y
    yf = fourTransMag(Y)
    return [X, Yunfiltered, xf[0:201], fourierFilter(yf)]


def fourierFilter(yf):
    # acts as a bandpass filter from 1 - 20 Hz, setting values <1 to 0 and removing frequencies past 50Hz.
    yf = yf[0:201]
    for i in range(10):
        yf[i] = 0
    return yf


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
    print(eqFour)
    print(maxVal)
    for i in range(len(eqFour)):
        weightedProfile[i] = eqFour[i] / maxVal
    return weightedProfile


def weightedFreqMag(eqFour, weightedProfile):
    # accepts a fourier profile equalized against neutral dataset and a frequency set. generates a score weighing in
    # favor of the weighted profile
    score = 0
    i = 0
    eqFour = eqFour[0:200]  # fix this
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
    threshScore = weightedFreqMag(equalizedDistress, weightedProfile) * 0.85
    return fourierFilter(weightedProfile), threshScore


def distressCheckFourier(currentFour, neutralProfile, weightedProfile, threshScore):
    eq = subtractFourier(currentFour, neutralProfile)
    score = weightedFreqMag(eq, weightedProfile)
    if score > threshScore:
        return True
    else:
        print("threshold not reached current value is " + str(score) + "\nrequires " + str(threshScore))
        return False


def calibrationV7Four(t, Hz, eogChan):
    query = input("please input 'y' if you want to display plots, enter if not.\n")
    if query == 'y':
        displayPlots = True
    else:
        displayPlots = False
    query = input("please input 'y' if you want audible prompts, enter if else.\n")
    if query == 'y':
        speech = True
    else:
        speech = False
    if speech:
        engine = initSpeechEngine()
    s = "Please look straight ahead for %d seconds. You will be signaled to stop." % t
    print(s)
    if speech:
        speakString(s, engine)
    time.sleep(5)
    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan, engine, speech)
    print("done.")
    time.sleep(1)
    s = "Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to stop." % t
    print(s)
    if speech:
        speakString(s, engine)
    time.sleep(5)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan, engine, speech)
    time.sleep(1)
    print("done.")
    weightedProfile, threshScore = makeFourierThresholds(Yneu, Ydis)
    if displayPlots:
        fig, plt, ax, line = initPlotFour(xfDis, yfNeu)
        print("displaying fourier of neutral..")
        if speech:
            speakString("displaying fourier of neutral..", engine)
        updatePlt(plt, line, yfNeu, Hz)
        input("press enter to continue.")
        print("displaying fourier of distress..")
        if speech:
            speakString("displaying fourier of distress..", engine)
        updatePlt(plt, line, yfDis, Hz)
        input("press enter to continue.")
        print("displaying weightedProfile..")
        if speech:
            speakString("displaying fourier of weighted profile..", engine)
        plt.xlim([0, 20])
        plt.ylim([0, 1])
        ax.clear()
        graph = plt.plot(xfDis, weightedProfile)[0]
        input("press enter to continue.")
        print("displaying raw voltage of neutral..")
        if speech:
            speakString("displaying raw voltage of neutral..", engine)
        ax.clear()
        graph = plt.plot(Xneu, Yneu)[0]
        plt.xlim([0, t])
        plt.ylim([0, 3.5])
        input("press enter to continue.")
        ax.clear()
        graph = plt.plot(Xneu, Ydis)[0]
        print("displaying raw voltage of distress..")
        if speech:
            speakString("displaying raw voltage of distress..", engine)
        input("press enter to continue.")
    filename = input("input filename, or none for default\n")
    if len(filename) < 1:
        filename = "calibration_profile_%dHz_%dseconds.cali" % (Hz, t)
    else:
        filename = filename + '.cali'
    f = open(filename, 'w')
    currentTime = str(datetime.now()).replace(' ', '_')
    f.write('threshold score' + '\t' + str(threshScore) + '\t' + 'current time:\t' + currentTime + '\n')
    f.write("time(s)\tneutral(raw)\tdistress(raw)\tfrequency(Hz)\tneutral(mag)\tdistress(mag)\tweighted profile\n")
    for i in range(len(Xneu)):
        if i < len(yfNeu):
            line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\t' + str(xfDis[i]) + '\t' + str(
                yfNeu[i]) + '\t' + str(yfDis[i]) + '\t' + str(weightedProfile[i]) + '\n'
        else:
            line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\n'
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
        for i in range(200):
            line = lines[i].split('\t')
            neutral.append(float(line[4].replace('\n', '')))
            weighted.append(float(line[6].replace('\n', '')))
        return threshScore, neutral, weighted
    except FileNotFoundError:
        print("no file found under this filename.")
        return False


def getFourierData(filename):
    # reads cali file, pulls neutral and distress fourier morphology.
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        header = lines[0]
        threshScore = float(header.split('\t')[1])
        freq = []
        neutral = []
        distress = []
        lines.pop(0)
        lines.pop(0)
        for i in range(200):
            line = lines[i].split('\t')
            freq.append(float(line[3].replace('\n', '')))
            neutral.append(float(line[4].replace('\n', '')))
            distress.append(float(line[5].replace('\n', '')))
        return freq,neutral, distress
    except FileNotFoundError:
        print("no file found under this filename.")
        return False


def initPlotFour(xf, yf, freqBounds=[0, 40], magBounds=[0, 1000]):
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
