from datetime import datetime
from eogCore import *
import time


def calibrationV7Four(t, Hz, eogChan):
    query = input("please input 'y' if you want to display plots, enter if not.\n")
    if query == 'y':
        displayPlots = True
    else:
        displayPlots = False
    engine = initSpeechEngine()
    s = "Please look straight ahead for %d seconds. You will be signaled to stop." % t
    print(s)
    speakString(s,engine)
    time.sleep(5)
    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan, engine)
    print("done.")
    time.sleep(1)
    s = "Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to stop." % t
    print(s)
    speakString(s, engine)
    time.sleep(5)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan, engine)
    time.sleep(1)
    print("done.")
    weightedProfile, threshScore = makeFourierThresholds(Yneu, Ydis)
    if displayPlots:
        fig, plt, ax, line = initPlotFour(xfDis, yfNeu)
        print("displaying fourier of neutral..")
        speakString("displaying fourier of neutral..", engine)
        updatePlt(plt, line, yfNeu, Hz)
        input("press enter to continue.")
        print("displaying fourier of distress..")
        speakString("displaying fourier of distress..", engine)
        updatePlt(plt, line, yfDis, Hz)
        input("press enter to continue.")
        print("displaying weightedProfile..")
        speakString("displaying fourier of weighted profile..", engine)
        plt.xlim([0, 50])
        plt.ylim([0, 1])
        ax.clear()
        graph = plt.plot(xfDis, weightedProfile)[0]
        input("press enter to continue.")
        print("displaying raw voltage of neutral..")
        speakString("displaying raw voltage of neutral..", engine)
        ax.clear()
        graph = plt.plot(Xneu, Yneu)[0]
        plt.xlim([0, t])
        plt.ylim([0, 3.5])
        input("press enter to continue.")
        ax.clear()
        graph = plt.plot(Xneu, Ydis)[0]
        print("displaying raw voltage of distress..")
        speakString("displaying raw voltage of distress..", engine)
        input("press enter to continue.")
    filename = input("input filename, or none for default\n")
    if len(filename) < 1:
        filename = "calibration_profile_%dHz_%dseconds.cali" % (Hz, t)
    else:
        filename = filename+'.cali'
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


if __name__ == "__main__":
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        exit()
    calibrationV7Four(10, 500, chanEOG)
