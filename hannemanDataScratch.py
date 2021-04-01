from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np

f = open('hannemanmar31', 'r')
x = []
yneu = []
ydis = []
for line in f:
    line = line.split('\t')
    if len(line) > 1:
        try:
            x.append(float(line[0]))
            yneu.append(float(line[1]))
            ydis.append(float(line[2]))
        except ValueError:
            pass
print(len(x))
print(len(yneu))
print(len(ydis))
N = 500 * 10
yf = fft(yneu)
xf = fftfreq(N, 1 / 500)[:N // 2]
print(len(yf))
print(len(xf))
plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))

plt.grid()

plt.show()
