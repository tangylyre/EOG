from numpy import linspace
import numpy as np
from numpy.fft import fftfreq
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt
from scipy.signal import blackman


def fourTrans(y, Hz):
    n = len(y)
    spacing = 1 / Hz
    yf = fft(y)
    xf = fftfreq(n, spacing)
    return xf, yf


f = open('josh.txt')
data = []
for line in f:
    if '\t' in line:
        val = line.split('\t')[0]
        data.append(val)
print(len(data))
xf, yf = fourTrans(data[60:], 500)
print(len(xf))
print(len(yf))
fig, a = plt.subplots()
plt.plot(xf, np.sqrt(yf.real ** 2 + yf.imag ** 2))
plt.grid()
a.set_ylim(0, 100)
a.set_xlim(0, 200)
a.set_ylabel('Magnitude (Volts)')
a.set_xlabel('Frequency (Hz)')
a.set_title('Fast Fourier Transform')

plt.show()
