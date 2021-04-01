from datetime import datetime
from eogCore import *
import time


def calibrationV6Four(t, Hz, eogChan):
    print("Please look straight ahead for %d seconds. You will be signaled to stop." % t)
    time.sleep(5)

    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)

    print("Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to "
          "stop." % t)
    time.sleep(5)
    print("done.")
    time.sleep(1)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan)

    return [Xneu, Yneu, Ydis, xfDis, yfNeu, yfDis]


def main():
    rf = 10
    hz = 500
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        return
    Xneu, Yneu, Ydis, xfDis, yfNeu, yfDis = calibrationV6Four(rf, hz, chanEOG)
    fig, plt, ax, line = initPlotFour(xfDis, yfNeu)
    print("displaying fourier of neutral..")
    updatePlt(plt, line, yfNeu, hz)
    input("press enter to continue.")
    print("displaying fourier of distress..")
    updatePlt(plt, line, yfDis, hz)
    input("press enter to continue.")
    print("displaying raw voltage of neutral..")
    ax.clear()
    graph = plt.plot(Xneu, Yneu)[0]
    plt.xlim([0, rf])
    plt.ylim([0, 3.5])
    input("press enter to continue.")
    graph.set_ydata(Ydis)
    print("displaying raw voltage of distress..")
    updatePlt(plt, line, Ydis, hz)
    input("press enter to continue.")
    query = input("write to file? (y/n)")
    weightedProfile, threshScore = makeFourierThresholds(Yneu, Ydis)
    print(weightedProfile)
    print(threshScore)
    if query == 'y':
        filename = input("input filename, or none for default\n")
        if len(filename) < 1:
            filename = "calibration_profile_%dHz_%dseconds.tsv" % (hz, rf)
        f = open(filename, 'w')
        currentTime = str(datetime.now()).replace(' ', '_')
        f.write(currentTime + '\n')
        f.write("time(s)\tneutral(raw)\tdistress(raw)\tfrequency(Hz)\tneutral(mag)\tdistress(mag)\n")
        for i in range(len(yfNeu)):
            line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\t' + str(xfDis[i]) + '\t' + str(
                yfNeu[i]) + '\t' + str(yfDis[i]) + '\n'
            f.write(line)
        f.close()


if __name__ == "__main__":
    main()