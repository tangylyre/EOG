import numpy as np
from scipy.fft import fft, ifft

def fourTransMag(y):
    yf = fft(y)
    mag = np.sqrt(yf.real ** 2 + yf.imag ** 2)
    return mag