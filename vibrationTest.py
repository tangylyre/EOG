from eogCore import *
import time

dac = initDAC()

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
