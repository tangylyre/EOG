from eogCore import initDAC, setVoltsNorm
from time import sleep
import adafruit_mcp4725 as DAC
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
# Initialize MCP4725.
try:
    dac = DAC.MCP4725(i2c)
except ValueError:
    dac = DAC.MCP4725(i2c, address=63)


motor = dac
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
