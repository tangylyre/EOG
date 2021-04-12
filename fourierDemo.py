from datetime import datetime
from eogCore import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from fourierCore import *


def main():
    rf = 10
    hz = 500
    Y = np.linspace(0, 0, hz)
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        return
    query = input("load calibration profile (1) or record new profile (2)")
    if query == '1':
        filename = filedialog.askopenfilename(title="Select a Calibration Profile",
                                              filetypes=(("calibration files",
                                                          "*.cali*"),
                                                         ("all files",
                                                          "*.*")))
        threshScore, neutral, weighted = calibrationRead(filename)
    else:
        filename = calibrationV7Four(rf, hz, chanEOG)
        threshScore, neutral, weighted = calibrationRead(filename)
    print("Calibration Profile Read Successfully!")
    threshDetect = False
    i = 0
    X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz)
    rfPopulate = rf * hz
    time.sleep(2)
    print("beginning to monitor..")
    while not threshDetect:
        c1 = chanEOG.voltage
        Y = popNdArray(c1, Y)
        yf = fourTransMag(Y)
        if i > rfPopulate:
            # this gates any distress signal false positives while the reading frame is being populated
            threshDetect = distressCheckFourier(yf, neutral, weighted, threshScore)
        i += 1
    print("threshold was exceeded!")
    query = input("write to file? (y/n)\n")
    if query == 'y':
        filename = input("input filename, or none for default")
        if len(filename) < 1:
            filename = "distress_flag_profile_%dHz_%dseconds.tsv" % (hz, rf)
        f = open(filename, 'w')
        i = 0
        f.write("time (s)\tEOG (volts)")
        for data in Y:
            f.write(str(i) + "\t" + str(data)+ '\n')
            i += 1 / hz
        f.close()


if __name__ == "__main__":
    main()
