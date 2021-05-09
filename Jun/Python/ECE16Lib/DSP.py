"""
DSP.py

@author: Jun Park (A15745118)
"""

import numpy as np
import scipy.signal as sig

"""
A module to provide common DSP filtering functionalities
"""

"""
Compute the L1-norm for 3 vectors: L1 = |ax| + |ay| + |az|
Note: Realistically, this function should be more general to any
number of input vectors, but we will only use it for 3.
"""
def l1_norm(ax, ay, az):
    return abs(ax) + abs(ay) + abs(az)

"""
Compute the moving average efficiently over a window 'win'
"""
def moving_average(x, win):
    ma = np.zeros(x.size)
    for i in np.arange(0,len(x)):
        if(i < win): # use mean until filter is "on"
            ma[i] = np.mean(x[:i+1])
        else:
            ma[i] = ma[i-1] + (x[i] - x[i-win])/win
    return ma

"""
Detrend the signal by removing the moving average
"""
def detrend(x, win=50):
    return x - moving_average(x, win)

"""
Compute the gradient of the signal
"""
def gradient(x):
    return np.gradient(x)

"""
Compute the power spectral density of the signal
"""
def psd(x, nfft, fs):
    return sig.welch(x, nfft=nfft, fs=fs)

"""
Create either high-pass or low-pass filters
"""
def create_filter(order, cutoff, btype, fs):
    b, a = sig.butter(order, cutoff, btype=btype, fs=fs)
    return b, a

"""
Filter the signal with the filter defined by the coefficients in b/a
"""
def filter(b, a, x):
  return sig.filtfilt(b, a, x)
    
"""
Count the number of peaks found between the lower and upper thresholds
"""
def count_peaks(x, thresh_low, thresh_high):
    peaks, _ = sig.find_peaks(x)
      
    count = 0
    locations = []
    for peak in peaks:
        if x[peak] >= thresh_low and x[peak] <= thresh_high:
            count += 1
            locations.append(peak)

    return count, locations