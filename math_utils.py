import numpy as np
import matplotlib.pyplot as plt

# Generic FFT function for only n coefficients
def n_fourier_coef(x, n):
    return np.fft.fft(x)[:n] / len(x)


"""
    Inputs:
        c -> exponential coefficients
    Outputs:
        a -> the cosine coefficients
        b -> the sine coefficients
"""
def exp_trig(c):
    N = len(c)
    a = np.zeros(N)
    b = np.zeros(N)
    a[0] = np.real(c[0])
    a[1:] = 2 * np.real(c[1:])
    b[1:] = 2 * np.imag(c[1:])

    return a, b

"""
    Inputs: 
        a -> cosine coefficients
        b -> sine coefficients
        P -> period of the original signal
        t_start -> starting time
        t_stop -> ending time
        Fs -> sampling frequency 
    Output:
        sig_recon -> Recontructed signal
        t -> time array corresponding to output signal

"""
def reconstruct(a, b, P, t_start, t_end, Fs):
    # Args check
    assert len(a) == len(b)

    # Generate time array
    t = np.linspace(t_start, t_end, int((t_end - t_start) * Fs))

    # Compute reconstructed signal
    sig_recon = t * 0
    w0 = 2 * np.pi / P
    for i in range(len(a)):
        sig_recon += a[i] * np.cos(w0 * i * t) + b[i] * np.sin(w0 * i * t)
    
    return t, sig_recon