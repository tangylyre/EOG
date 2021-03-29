from datetime import datetime
from eogCore import *
from tkinter import filedialog
import matplotlib.pyplot as plt

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
        f = open(filedialog.askopenfilename(title="Select a Calibration Profile",
                                            filetypes=(("calibration files",
                                                        "*.cali*"),
                                                       ("all files",
                                                        "*.*"))))
        for line in f:
            try:
                thresh = int(line)
                break
            except ValueError:
                print("invalid file format. proceeding to calibrate manually..")
                thresh = calibrationV6Diff(rf, hz, chanEOG)
    else:
        thresh = calibrationV6Diff(rf, hz, chanEOG)
    threshDetect = False
    i = 0
    rfPopulate = rf * hz
    X = np.linspace(0, rf, hz)
    graph = plt.plot(X, Y)[0]
    plt.xlim([0, rf])
    plt.ylim([0, 3.5])
    while not threshDetect:
        c1 = chanEOG.voltage
        Y[-1] = c1
        for x in range(len(Y) - 1):
            Y[x] = Y[x + 1]
        graph.set_ydata(Y)
        plt.draw()
        plt.pause(1 / hz)
        if i > rfPopulate:
            # this gates any distress signal false positives while the reading frame is being populated
            difMax, difMin, difMean = getVoltDif(Y)
            threshDetect = evaluateThreshold(difMean, difMax, thresh)
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
            f.write("%0.2f\t%0.2f" % i, data)
            i += 1 / hz
        f.close()


if __name__ == "__main__":
    main()
