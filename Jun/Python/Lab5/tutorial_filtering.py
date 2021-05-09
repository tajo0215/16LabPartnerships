"""
Lab 5 Tutorial 2: tutorial_filtering.py

@author: Jun Park (A15745118)
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

def load_data(filename):
    return np.genfromtxt(filename, delimiter=",")

# Compute the L1 norm for vectors ax, ay, az (L1=|ax|+|ay|+|az|)
def L1_norm(ax, ay, az):
    return abs(ax) + abs(ay) + abs(az)

# Compute the Moving Average Effectively
def moving_average(x, win):
    ma = np.zeros(x.size)
    for i in np.arange(0,len(x)):
        if(i < win): # use mean until filter is "on"
            ma[i] = np.mean(x[:i+1])
        else:
            ma[i] = ma[i-1] + (x[i] - x[i-win])/win
    return ma

# Detrend the Signal
def detrend(x, win=50):
    return x - moving_average(x, win)

# Count the Number of Peaks
def count_peaks(x, thresh_low, thresh_high):
    peaks, _ = sig.find_peaks(x)
    count = 0
    locations = []
    
    for peak in peaks:
        if x[peak] >= thresh_low and x[peak] <= thresh_high:
            count += 1
            locations.append(peak)
            
    return count, locations

# Load the data as a 500x4 ndarray
data = load_data("./data/8steps_10s_50hz.csv")
t = data[:,0]
t = (t - t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]
L1 = L1_norm(ax, ay, az)

# plt.subplot(411)
# plt.plot(ax)
# plt.subplot(412)
# plt.plot(ay)
# plt.subplot(413)
# plt.plot(az)
# plt.subplot(414)
# plt.plot(L1)
# plt.show()

ma = moving_average(L1, 20)
# plt.plot(L1, 'b')
# plt.plot(ma, 'r')
# plt.show()

dt = detrend(ma)
# plt.subplot(211)
# plt.plot(ma)
# plt.subplot(212)
# plt.plot(dt)
# plt.show()

# Compute the Gradient
grad = np.gradient(dt)

# plt.subplot(211)
# plt.plot(dt)
# plt.subplot(212)
# plt.plot(grad)
# plt.show()

# Power Spectral Density
fs = 50 # sampling rate
freqs, power = sig.welch(az, nfft=len(az), fs=fs)
# plt.subplot(211)
# plt.plot(az)
# plt.subplot(212)
# plt.plot(freqs, power)
# plt.show()

# Low-pass Filter Design
bl, al = sig.butter(3, 1, btype="lowpass", fs=fs)

w, h = sig.freqz(bl, al, fs=50)
# plt.plot(w, 20 * np.log10(abs(h)))
# plt.show()

# Low-pass Filter the Signal
lp = sig.lfilter(bl, al, dt)

# plt.subplot(211)
# plt.plot(dt)
# plt.subplot(212)
# plt.plot(lp)
# plt.show()

lp2 = sig.filtfilt(bl, al, dt)

# plt.subplot(211)
# plt.plot(dt)
# plt.subplot(212)
# plt.plot(lp2)
# plt.show()

thresh_low = 25
thresh_high = 100
count, peaks = count_peaks(lp2, thresh_low, thresh_high)

plt.plot(t, lp2)
plt.title("Detected Peaks = %d" % count)
plt.plot(t[peaks], lp2[peaks], 'rx')
plt.plot(t, [thresh_low]*len(lp2), "b--")
plt.plot(t, [thresh_high]*len(lp2), "b--")
plt.show()
