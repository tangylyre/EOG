from datetime import datetime
from eogCore import *


# this is the same as readingframe v1 but with fourier implementation.


def main():
    chanEOG = initEOG()
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        return
    try:
        file = str(input("Input the name of the file you'd like to write to:\n"))
        if file == '':
            file = 'FourierVis_%s' % datetime.now()
    except ValueError:
        file = 'FourierVis_%s' % datetime.now()
    file.replace(' ', '_')
    hz = 500
    rf = 10
    X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz)
    f = open(file, 'w+')
    f.write("\n begin log for calibration v1")
    f.write(str(datetime.now()))
    q = False
    try:
        while not q:
            c1 = chanEOG.voltage
            Y = popNdArray(c1, Y)
            yf = fourTransMag(Y)
            try:
                updatePlt(plt, line, yf, hz)
            except KeyboardInterrupt:
                plt.close()
                f.close()
                break
            f.write(str(c1) + '\n')
    except KeyboardInterrupt:
        plt.close()
        f.close()
    print("successfully quit.")


if __name__ == '__main__':
    main()
