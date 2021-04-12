from datetime import datetime
from eogCore import *
from fourierCore import *

# this program will operate on a 10s reading frame and display the fourier transform of this frame indefinitely.
# as of now there is no quit function, press and hold ctrl c to quit.


def fourierVisualizer():
    chanEOG = initEOG()
    currentTime = str(datetime.now()).replace(' ', '_')
    if not chanEOG:
        print("failed to read EOG channel; please check circuit config and bugfix initEOG().")
        return
    try:
        file = str(input("Input the name of the file you'd like to write to:\n"))
        if file == '':
            file = 'FourierVis'
    except ValueError:
        file = 'FourierVis'
    file.replace(' ', '_')
    hz = 500
    rf = 10
    X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz)
    f = open(file, 'w+')
    f.write("\n begin log for calibration v1")
    f.write(str(datetime.now())+'\n')
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
    fourierVisualizer()
