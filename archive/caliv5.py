from datetime import datetime
from eogCore import *
import time


def pullFourierProfile(t, Hz, eogChan):
    numFrames = t * Hz
    i = 0
    j = 0
    X, Y, xf, yf = initVals(t, Hz)
    fourierAveraged = yf
    dataPoints = len(Y)
    print(dataPoints)
    print(numFrames)
    while i <= numFrames:
        c1 = eogChan.voltage
        Y = popNdArray(c1, Y)
        if i > dataPoints:
            j += 1
            # print(fourTransMag(Y))
            # print(fourierAveraged)
            fourierAveraged = fourierAveraged + fourTransMag(Y)
            # print(yf)
        i += 1
        time.sleep(1 / Hz)
        currentTime = int(i) / int(Hz)
        print("%d dataframes were averaged." %j)
        print("seconds elapsed: %0.2f" % currentTime)
    return fourierAveraged/j


def calibrationV3(t, Hz, eogChan):
    print("Please look straight ahead for %d seconds. You will be signaled to stop." % t)
    time.sleep(5)

    neutral = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)

    print("Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to "
          "stop." % t)
    time.sleep(5)
    print("done.")
    time.sleep(1)
    distress = pullFourierProfile(t, Hz, eogChan)

    return [neutral, distress]


def main():
    rf = 20
    hz = 500
    X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz)
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        return
    [neutral, distress] = calibrationV3(rf, hz, chanEOG)
    print(neutral)
    updatePlt(plt, line, neutral, hz)
    input("press enter to continue.")
    print(distress)
    updatePlt(plt, line, distress, hz)
    input("press enter to continue.")
    query = input("write to file? (y/n)")
    if query == 'y':
        filename = input("input filename, or none for default")
        if len(filename) < 1:
            currentTime = str(datetime.now()).strip()
            filename = "calibration_profile_%dHz_%dseconds_%s.tsv" % (hz, rf, currentTime)
        f = open(filename, 'w')
        f.write("frequency(Hz)\tneutral\tdistress\n")
        for i in range(len(neutral)):
            line = str(xf[i]) + '\t' + str(neutral[i]) + '\t' + str(distress[i]) + '\n'
            f.write(line)
        f.close()


if __name__ == "__main__":
    main()