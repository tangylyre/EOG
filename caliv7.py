from datetime import datetime
from eogCore import *
import time


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
    dis = Ydis
    time.sleep(1)
    print("done.")
    weightedProfile, threshScore = makeFourierThresholds(Yneu, Ydis)
    fig, plt, ax, line = initPlotFour(xfDis, yfNeu)
    print("displaying fourier of neutral..")
    updatePlt(plt, line, yfNeu, Hz)
    input("press enter to continue.")
    print("displaying fourier of distress..")
    updatePlt(plt, line, yfDis, Hz)
    input("press enter to continue.")
    print("displaying weightedProfile..")
    plt.xlim([0, 50])
    plt.ylim([0, 1])
    updatePlt(plt, line, weightedProfile, Hz)
    input("press enter to continue.")
    print("displaying raw voltage of neutral..")
    ax.clear()
    graph = plt.plot(Xneu, Yneu)[0]
    plt.xlim([0, t])
    plt.ylim([0, 3.5])
    input("press enter to continue.")
    graph.set_ydata(dis)
    print("displaying raw voltage of distress..")
    input("press enter to continue.")
    filename = input("input filename, or none for default\n")
    if len(filename) < 1:
        filename = "calibration_profile_%dHz_%dseconds.cali" % (Hz, t)
    f = open(filename, 'w')
    currentTime = str(datetime.now()).replace(' ', '_')
    f.write('threshold score' + '\t' + str(threshScore) + '\t' + 'current time:\t' + currentTime + '\n')
    f.write("time(s)\tneutral(raw)\tdistress(raw)\tfrequency(Hz)\tneutral(mag)\tdistress(mag)\tweighted profile\n")
    for i in range(len(yfNeu)):
        line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(dis[i]) + '\t' + str(xfDis[i]) + '\t' + str(
            yfNeu[i]) + '\t' + str(yfDis[i]) + '\t' + str(weightedProfile[i]) + '\n'
        f.write(line)
    f.close()
    return filename


if __name__ == "__main__":
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        exit()
    calibrationV7Four(10, 500, chanEOG)
