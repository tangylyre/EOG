from eogCore import initDAC, setVoltsNorm
from time import sleep
motor = initDAC()
i = 0.1
x = 0
try:
    while True:
        if x >= 1:
            i = -0.1
        elif x <= 0:
            i = 0.1
        setVoltsNorm(motor, x)
        x += i
        print(x)
        sleep(1)
except KeyboardInterrupt:
    setVoltsNorm(motor, 0)
    print("stopping..")
