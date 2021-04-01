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
    print("done.")
    time.sleep(1)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan)
    weightedProfile, threshScore = makeFourierThresholds(Yneu, Ydis)
    query = input("write to file? (y/n)\n")
    if query == 'y':
        filename = input("input filename, or none for default\n")
        if len(filename) < 1:
            filename = "calibration_profile_%dHz_%dseconds.tsv" % (hz, rf)
        f = open(filename, 'w')
        currentTime = str(datetime.now()).replace(' ', '_')
        f.write('threshold score' + '\t' + 'current time:\t' + currentTime + '\n')
        f.write("time(s)\tneutral(raw)\tdistress(raw)\tfrequency(Hz)\tneutral(mag)\tdistress(mag)\tweighted profile\n")
        for i in range(len(yfNeu)):
            line = str(Xneu[i]) + '\t' + str(Yneu[i]) + '\t' + str(Ydis[i]) + '\t' + str(xfDis[i]) + '\t' + str(
                yfNeu[i]) + '\t' + str(yfDis[i]) + '\t' + str(weightedProfile[i]) + '\n'
            f.write(line)
        f.close()
    else:
        filename = ''
    return filename


if __name__ == "__main__":
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        exit()
    calibrationV7Four(10, 500, chanEOG)
