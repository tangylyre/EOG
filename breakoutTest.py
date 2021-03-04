from eogCore import initDAC, setVoltsNorm

motor = initDAC()
i = 0.1
x = 0
try:
    while True:
        if x == 1 or x == 0:
            i *= -1
        setVoltsNorm(motor, x)
        x += i
        print(x)
except KeyboardInterrupt:
    setVoltsNorm(motor, 0)
    print("stopping..")
