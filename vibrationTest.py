from eogCore import *
import time

dac = initDAC()

# depreciated method for operating breadboard breakout board. this will not work on our current build.


try:
    i = 0
    while True:
        if i >= 1:
            i = 0
        time.sleep(1)
        setVoltsNorm(dac, i)
        i += 0.1


except KeyboardInterrupt:
    pass
