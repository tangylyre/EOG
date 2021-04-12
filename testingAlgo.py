from eogCore import *
from fourierCore import *
from utilitiesCore import *

hz = 500
rf = 10
X, Y, xf, yf = initVals(rf, hz)
freq, neutral, distress = getFourierData("joshcali1.cali")
X, Y, xf, yf, fig, plt, ax, line = initPlot(rf, hz)
updatePlt(plt, line, neutral, hz)
input('press enter')
updatePlt(plt, line, distress, hz)
normalize = subtractFourier(distress, neutral)
input('press enter')
updatePlt(plt, line, normalize, hz)
input('press enter')
