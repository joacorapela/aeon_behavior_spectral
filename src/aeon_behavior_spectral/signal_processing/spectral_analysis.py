import numpy as np
from numpy.fft import fft


def estimate_power_spectrum(x, fs, T):
    dt = 1.0 / fs
    xf = fft(x - x.mean())                      # Compute Fourier transform
    Sxx = 2 * dt ** 2 / T * (xf * np.conj(xf))  # Compute spectrum
    Sxx = Sxx[:int(len(x) / 2)]                 # Ignore negative frequencies
    Sxx = Sxx.real

    df = 1 / T                                  # Determine freq resolution
    fNQ = 1 / dt / 2                            # Determine Nyquist frequency
    freqs = np.arange(0, fNQ, df)               # Construct frequency axis

    return Sxx, freqs
