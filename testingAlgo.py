from eogCore import *
from fourierCore import *
from utilitiesCore import *

hz = 500
rf = 10
X, Y, xf, yf = initVals(rf, hz)
freq, neutral, distress = getFourierData("joshcali1.cali")
fig, plt, ax, line = initPlotFour(freq, neutral)
updatePlt(plt, line, neutral, hz)
input('press enter')
updatePlt(plt, line, distress, hz)
normalize = subtractFourier(distress, neutral)
input('press enter')
updatePlt(plt, line, normalize, hz)
input('press enter')
weightedProf = makeWeightProfile(normalize)
updatePlt(plt, line, weightedProf, hz)
input('press enter')
