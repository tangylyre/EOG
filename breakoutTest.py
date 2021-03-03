# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.
import board
import busio
import time
import adafruit_mcp4725
import keyboard as key

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725.
try:
    dac = adafruit_mcp4725.MCP4725(i2c)
except ValueError:
    dac = adafruit_mcp4725.MCP4725(i2c, address=63)
# Optionally you can specify a different addres if you override the A0 pin.
# amp = adafruit_max9744.MAX9744(i2c, address=0x63)

# There are a three ways to set the DAC output, you can use any of these:
dac.value = 65535  # Use the value property with a 16-bit number just like
# the AnalogOut class.  Note the MCP4725 is only a 12-bit
# DAC so quantization errors will occur.  The range of
# values is 0 (minimum/ground) to 65535 (maximum/Vout).

dac.raw_value = 4095  # Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).

dac.normalized_value = 1.0  # Use the normalized_value property to set the
# output with a floating point value in the range
# 0 to 1.0 where 0 is minimum/ground and 1.0 is
# maximum/Vout.
global q
q = False


def terminate():
    global q
    q = True
    return


# Main loop will go up and down through the range of DAC values forever.
while not q:
    # Go up the 12-bit raw range.
    print("Going up 0-3.3V...")
    i = 0.05
    while i < 0.90:
        if key.is_pressed('esc'):
            q = True
            print('flag')
        dac.normalized_value = i
        i += 0.1
        time.sleep(0.05)
    # Go back down the 12-bit raw range.
    print("Going down 3.3-0V...")
    while i > 0.10:
        try:
            print(i)
            dac.normalized_value = i
            i -= 0.1
            time.sleep(0.05)
        except KeyboardInterrupt:
            break
dac.normalized_value = 0
print('finished')
