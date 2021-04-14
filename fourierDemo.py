from tkinter import filedialog
from eogCore import *
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
    else:
        speech, engine, filename = calibrationV7Four(rf, hz, chanEOG)
    q = False
    while not q:
        fourierMonitor(chanEOG, filename, engine, speech)
        query = input("quit? y/n\n")
        if query == 'y':
            q = True


if __name__ == "__main__":
    main()
