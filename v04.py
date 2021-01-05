#Oculert V0.2
#Alexander Humen, Jeffrey Frese, Michael McCarney, and Mark Thibeault

####################---Import all relevant packages
import os
import numpy
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pygame import mixer  # Load the popular external library
import pickle # Rick
import matplotlib.pyplot as plt
from scipy import signal
import scipy

# BLUETOOTH PACKAGES I MAY NEED TO REMOVE
# sudo apt uninstall bluetooth pi-bluetooth bluez blueman

####################---Importing Data

###---This is for saving data
#with open('pattern.pkl','wb') as f:
#    pickle.dump([pattern, data],f)

###---This is for opening data
with open('pattern.pkl','rb') as f:
    pattern, data = pickle.load(f)
pattern = pattern - 1.65

####################---Reading the GPIO
    
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan1 = AnalogIn(mcp, MCP.P0)
chan2 = AnalogIn(mcp, MCP.P1)

###################---Making the beep

mixer.init()
mixer.music.load('/home/pi/Desktop/beep.mp3')

###################---Recording the data for 10 seconds

data = numpy.zeros(2000)
#data1 = numpy.zeros(2000)
#data2 = numpy.zeros(2000)
print('start')

t=time.time()
for x in range(len(data)):
    time.sleep(0.0018)
    #data1[x] = chan1.voltage
    #data2[x] = chan2.voltage
    data[x] = numpy.mean([chan1.voltage,chan2.voltage])
                             
print('elapsed initial time: '+ str(time.time()-t))

data = data - 1.65

####################---Recording the data indefinitely

newbatch = numpy.zeros(200)
data_storage = numpy.zeros(180000)
peaks_storage = numpy.zeros(3600)
store_index=0
epsteindidntkillhimself = True
while epsteindidntkillhimself==1:
    
    t=time.time()
    crosscor = numpy.correlate(data,pattern)
    peaks = scipy.signal.find_peaks(crosscor,height=100,distance=100)
    peaks_thresh = scipy.signal.find_peaks(crosscor,height=1,distance=100)
    # print('elapsed correlation time: '+ str(time.time()-t))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    
    if len(peaks[0]) > 2:
        mixer.music.play()
        # epsteindidntkillhimself = 0
        print('PATTERN')
    elif len(peaks_thresh[0]) > 2:
        peaks_thresh[1]["peak_heights"].sort()
        peaks_storage[store_index] = sorted(peaks_thresh[1]["peak_heights"],reverse=True)[2]
        
    for x in range(len(newbatch)):
        newbatch[x] = numpy.mean([chan1.voltage,chan2.voltage])
        time.sleep(0.0018)
    newbatch = newbatch - 1.65
    data = numpy.concatenate((data[len(newbatch):],newbatch))
    data_storage[store_index*50:store_index*50+50]=newbatch[0::4]
    store_index+=1
    #del crosscor
    #del peaks
    #print('elapsed for loop time: '+ str(time.time()-t))
    print(str(peaks[0]))