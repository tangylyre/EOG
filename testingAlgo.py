from eogCore import *
from fourierCore import *
from utilitiesCore import *

hz = 500
rf = 10
X, Y, xf, yf = initVals(rf, hz)
freq, neutral, distress = getFourierData("joshcali1.cali")
print(distress)
fig, plt, ax, line = initPlotFour(freq, neutral)
updatePlt(plt, line, neutral, hz)
input('neutral')
updatePlt(plt, line, distress, hz)
normalize = subtractFourier(distress, neutral)
input('distress')
updatePlt(plt, line, normalize, hz)
input('difference of magnitude')
#weightedProf = makeWeightProfile(normalize)
#plt.xlim([0, 40])
#plt.ylim([0, 1])
#updatePlt(plt, line, weightedProf, hz)
input('normalized difference')
print(distress)
weightedProf, threshScore = makeFourierThresholds(distress, neutral)
print(threshScore)
updatePlt(plt, line, weightedProf, hz)
input('normalized difference method')
