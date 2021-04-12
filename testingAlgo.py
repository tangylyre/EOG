from eogCore import *
from fourierCore import *
from utilitiesCore import *

hz = 500
rf = 10
X, Y, xf, yf = initVals(rf, hz)
neutral, distress = getFourierData("joshcali1.cali")
print(xf[0:200])
fig, plt, ax, line = initPlotFour(xf[0:200], neutral)
input('press enter')
updatePlt(plt, line, distress, hz)
normalize = subtractFourier(distress, neutral)
input('press enter')
updatePlt(plt, line, normalize, hz)
input('press enter')
