from datetime import datetime
from eogCore import *
import time


def pullFourierProfile(t, Hz, eogChan):
    numFrames = t * Hz
    i = 0
    j = 0
    xf = fftfreq(numFrames, 1 / Hz)
    Y = []
    while i < numFrames:
        i += 1
        c1 = eogChan.voltage
        Y.append(c1)
        time.sleep(1 / Hz)
        currentTime = int(i) / int(Hz)
        print("%d dataframes were averaged." % j)
        print("seconds elapsed: %0.2f" % currentTime)
    yf = fourTransMag(Y)
    return [xf, yf]


def calibrationV3(t, Hz, eogChan):
    print("Please look straight ahead for %d seconds. You will be signaled to stop." % t)
    time.sleep(5)

    [xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)

    print("Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to "
          "stop." % t)
    time.sleep(5)
    print("done.")
    time.sleep(1)
    [xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan)

    return [xfDis, yfNeu, yfDis]


def main():
    rf = 10
    hz = 500
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        return
    xfDis, yfNeu, yfDis = calibrationV3(rf, hz, chanEOG)
    fig, plt, ax, line = initPlotFour(xfDis, yfNeu)
    print(yfNeu)
    updatePlt(plt, line, yfNeu, hz)
    input("press enter to continue.")
    print(yfDis)
    updatePlt(plt, line, yfDis, hz)
    input("press enter to continue.")
    query = input("write to file? (y/n)")
    if query == 'y':
        filename = input("input filename, or none for default")
        if len(filename) < 1:
            currentTime = str(datetime.now()).strip()
            filename = "calibration_profile_%dHz_%dseconds_%s.tsv" % (hz, rf, currentTime)
        f = open(filename, 'w')
        f.write("frequency(Hz)\tneutral\tdistress\n")
        for i in range(len(yfNeu)):
            line = str(xfDis[i]) + '\t' + str(yfNeu[i]) + '\t' + str(yfDis[i]) + '\n'
            f.write(line)
        f.close()


if __name__ == "__main__":
    main()
