from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from eogCore import *


# this script will monitor voltage with respect to time in a 10 second reading frame, indefinitely.
# there is no exit function yet, press and hold ctrl c to end the program.

def voltageVisualizer():
    chan1 = initEOG()
    Hz = 500
    Rf = 10
    x = 0
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    c1 = 0
    t = 0
    X = np.linspace(0, Rf, Hz)
    Y = np.linspace(0, 0, Hz)
    graph = plt.plot(X, Y)[0]
    plt.xlim([0, Rf])
    plt.ylim([0, 3.5])
    fi = "voltage_visualizer_datetime.now()"
    currentTime = str(datetime.now()).replace(' ', '_')
    try:
        file = str(input("Input the name of the file you'd like to write to:\n"))
        if file == '':
            file = 'VoltsVis'
    except ValueError:
        file = 'VoltsVis'
    file.replace(' ', '_')
    f = open(file, 'w')
    currentTime = str(datetime.now()).replace(' ', '_')
    f.write(currentTime + '\n')
    f.write("\n begin log for calibration v1")
    f.write(file)

    q = False
    try:
        while not q:
            c1 = chan1.voltage
            Y[-1] = c1
            for x in range(len(Y) - 1):
                Y[x] = Y[x + 1]
            graph.set_ydata(Y)
            plt.draw()
            plt.pause(1 / Hz)
            f.write(str(c1) + '\n')
    except KeyboardInterrupt:
        f.close()
        pass
    print("done!")


if __name__ == '__main__':
    voltageVisualizer()