from datetime import datetime
import time
from utilitiesCore import *


# this set of methods encompasses all the necesary calculations for a fourier analysis approach to EOG data.

def fourTransMag(y):
    # calculates the magnitude (non imaginary values) and returns it.
    # fft returns imaginary data which is often difficult to visualize & interpret.
    yf = fft(y)
    mag = np.sqrt(yf.real ** 2 + yf.imag ** 2)
    return mag


def pullFourierProfile(t, Hz, eogChan, voiceEngine, speech):
    # this is a method used within loops that prompts the user to undergo one collection of the targetted t-time.
    # this will collect data with respect to t and hz, and return all relevant datapoints and fourier transform.
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
    yf = fourTransMag(Y)
    return [X, Y, xf[0:200], fourierFilter(yf)]


def fourierFilter(yf):
    # acts as a bandpass filter from 1 - 20 Hz, setting values <1 to 0 and removing frequencies past 50Hz.
    yf = yf[0:200]
    for i in range(10):
        yf[i] = 0
    return yf


def subtractFourier(list1, list2):
    # runs through a numpy array and subtracts list 2 from list 1 element by element.
    # if the value is negative, just make it zero. This will make downstream of weighted frequencies.
    list1 = fourierFilter(list1)
    list2 = fourierFilter(list2)
    subtracted = np.zeros(len(list1))
    if len(list1) == len(list2):
        for i in range(len(list1)):
            val1 = list1[i]
            val2 = list2[i]
            subtracted[i] = val1 - val2
            if subtracted[i] < 0:
                subtracted[i] = 0
        return subtracted
    else:
        print("unequal list length, mismatch as follows:")
        print(len(list1))
        print(len(list2))
        return False


def makeWeightProfile(eqFour):
    # accepts a normalized equalized profile, assigns each frequency a weight from 0 - 1 in relation to this numpy
    # array's maxima.
    weightedProfile = np.zeros(len(eqFour))
    maxVal = np.amax(eqFour)
    for i in range(len(eqFour)):
        current = eqFour[i]
        # possibly decrease sensitivity by including sqrt function
        weightedProfile[i] = current / maxVal
    return weightedProfile


def weightedPower(fourierProf, weightedProf):
    i = 0
    power = 0
    while i < len(fourierProf):
        valCurrent = fourierProf[i]
        valWeight = weightedProf[i]
        power += valCurrent * valWeight
        i += 1
    return power


def weightedPowerTolerant(fourierProf, weightedProf):
    # this func is the same as weighted power, but i square root each weighted profile value to move it closer to 1,
    # should be more tolerant of unexpected frequencies.
    i = 0
    power = 0
    while i < len(fourierProf):
        valCurrent = fourierProf[i]
        valWeight = np.sqrt(weightedProf[i])
        power += valCurrent * valWeight
        i += 1
    return power


def distressCheckFourierV2(equalized, weightedProfile, threshScore):
    # this function is used to repeatedly check the current reading frame to see
    # if it exceeds the threshScore with respect to neutral profile and weighted profile.
    score = weightedPowerTolerant(equalized, weightedProfile)
    # score = weightedPower(equalized, weightedProfile)
    if score > threshScore:
        return True
    else:
        print("threshold not reached current value is " + str(score) + "\nrequires " + str(threshScore))
        return False


def getFourierData(filename):
    # reads cali file, pulls neutral and distress fourier morphology.
    try:
        f = open(filename, 'r')
        lines = f.readlines()
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
        return freq, neutral, distress
    except FileNotFoundError:
        print("no file found under this filename.")
        return False


def makeThreshV2(filename):
    freq, neutral, distress = getFourierData(filename)
    normalize = subtractFourier(distress, neutral)
    weightedProf = makeWeightProfile(normalize)
    threshScore = weightedPower(fourierFilter(distress), fourierFilter(weightedProf)) * 0.065
    return threshScore, weightedProf, neutral


def calibrationV8Four(t, Hz, eogChan):
    # acts as a main, invokes the pullFourierProfiles() method to collect data once for neutral and once for distress.
    # uses this to generate a threshold score related to the power generated by a given fourier transform.
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
    engine = initSpeechEngine()
    s = "Please look straight ahead for %d seconds. You will be signaled to stop." % t
    print(s)
    if speech:
        speakString(s, engine)
    time.sleep(5)
    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan, engine, speech)
    print("done.")
    time.sleep(1)
    s = "Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to stop." \
        % t
    print(s)
    if speech:
        speakString(s, engine)
    time.sleep(5)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan, engine, speech)
    time.sleep(1)
    print("done.")
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
    f.write('current time:\t' + currentTime + '\n')
    f.write("time(s)\tneutral(raw)\tdistress(raw)\tfrequency(Hz)\tneutral(mag)\tdistress(mag)\tweighted profile\n")
    for i in range(len(Xneu)):
        if i < len(yfNeu):
            line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\t' + str(xfDis[i]) + '\t' + str(
                yfNeu[i]) + '\t' + str(yfDis[i]) + '\n'
        else:
            line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\n'
        f.write(line)
    f.close()
    threshScore, weightedProf, neutral = makeThreshV2(filename)
    if speech:
        speakString("displaying fourier of weighted profile..", engine)
    if displayPlots:
        plt.ylim([0, 1])
        ax.clear()
        graph = plt.plot(xfDis, weightedProf)[0]
        input("press enter to continue.")
        plt.close()
    return threshScore, weightedProf, neutral, speech, engine


def fourierMonitorV2(chanEOG, threshScore, weightedProf, neutral, engine, speech, graph=False, writeLogs=False):
    # this is the implementation of a fourier based monitoring protocol,
    # whose method ends if the threshold generated based of calibration is exceeded.
    #global line
    rf = 10
    hz = 500
    print("Calibration Profile Read Successfully!")
    threshDetect = False
    i = 0
    if graph:
        X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz, freqBounds=[0, 40], magBounds=[0, 100])
    if writeLogs:
        logTime = []
        logVolts = []
    rfPopulate = rf * hz
    time.sleep(2)
    print("beginning to monitor..")
    while not threshDetect:
        c1 = chanEOG.voltage
        Y = popNdArray(c1, Y)
        yf = fourTransMag(Y)
        if i > rfPopulate and i % 5 == 0:
            # this gates any distress signal false positives while the reading frame is being populated
            equalized = subtractFourier(yf, neutral)
            threshDetect = distressCheckFourierV2(equalized, weightedProf, threshScore)
            if graph:
                updatePlt(plt, line, fourierFilter(equalized), hz)
            else:
                time.sleep(1/hz)
        else:
            time.sleep(1 / hz)
        i += 1
        if writeLogs:
            logTime.append(i*(1/hz))
            logVolts.append(c1)
    print("threshold was exceeded!")
    if speech:
        speakString("i need help", engine)
    if writeLogs:
        filename = input("input filename, or none for default")
        if len(filename) < 1:
            filename = "distress_flag_profile_%dHz_%dseconds.tsv" % (hz, rf)
        f = open(filename, 'w')
        i = 0
        f.write("time (s)\tEOG (volts)")
        for data in logVolts:
            f.write(str(i) + "\t" + str(data) + '\n')
            i += 1 / hz
        f.close()
