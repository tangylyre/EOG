from fourierCore import *

# this set of methods provides the means to analyze reading frame data with respect to time and voltage.
# frankly, this set is incomplete but may provide some insight as to how to approach analyses bypassing the
# fourier transform; but fourier is cooler and can filter a lot of auxillary noise the EOG picks up on.

def getVoltDif(V):
    # this function takes list V and compares them against the previous, making dif an n-1 length list.
    # the extrema of this list is used to generate calibration parameters.
    dif = []
    numPoints = len(V)
    for i in range(numPoints):
        current = V[i]
        if i > 0:
            dif.append(abs(current - prev))
        prev = current
    difMax = max(dif)
    difMin = min(dif)
    difMean = sum(dif) / (numPoints - 1)
    return difMax, difMin, difMean


def generateThreshold(neutralMax, distressMean, distressMax):
    # makes a threshold of voltage differential with respect to maxima and minima of distress and neutral.
    thresh = distressMean
    while thresh < neutralMax + 0.1 and thresh < distressMax - 0.1:
        thresh += 0.01
    return thresh


def evaluateThreshold(difMean, difMax, thresh):
    # helper method checks whether differential threshold is exceeded.
    # modify this formula dramatically if we're running with voltage differential
    evalNum = difMean * .75 + difMax * .25
    if evalNum > thresh:
        return True
    else:
        return False


def calibrationV6Diff(t, Hz, eogChan):
    # calibration for voltage approach. calls pullFourierProfile; try to make your own method if you plan on exploring
    # the voltage differential approach, because some of these methods are optimized towards fourier performance.
    print("Please look straight ahead for %d seconds. You will be signaled to stop." % t)
    time.sleep(5)
    [Xneu, Yneu, xfNeu, yfNeu] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)
    print("Please move between the upper and lower poles as fast as you can for %d seconds. You will be signaled to "
          "stop." % t)
    time.sleep(5)
    [Xdis, Ydis, xfDis, yfDis] = pullFourierProfile(t, Hz, eogChan)
    print("done.")
    time.sleep(1)
    neuMax, neuMin, neuMean = getVoltDif(Yneu)
    disMax, disMin, disMean = getVoltDif(Ydis)
    thresh = generateThreshold(neuMax, disMean, disMax)
    query = input('Write to file? (y/n)\n')
    if query == 'y':
        query = input('File name?\n')
        if len(query) == 0:
            fn = 'defaultProfile.cali'
        else:
            fn = query + '.cali'
        f = open(fn, 'w')
        f.write(str(thresh))
        f.close()
    return thresh
