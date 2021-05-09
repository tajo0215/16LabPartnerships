"""
Lab 5 Tutorial 2: tutorial_dsp_module.py

@author: Jun Park (A15745118)
"""


import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt
import numpy as np

fs = 50      # sampling rate
t_low = 25   # lower peak threshold
t_high = 100 # upper peak threshold

def load_data(filename):
    return np.genfromtxt(filename, delimiter=",")

# Load the data as a 500x4 ndarray
data = load_data("./data/8steps_10s_50hz.csv")
t = data[:,0]
t = (t - t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]

l1 = filt.l1_norm(ax, ay, az)                      # Compute the L1-Norm
ma = filt.moving_average(l1, 20)                   # Compute Moving Average
dt = filt.detrend(ma)                              # Detrend the Signal
grad = filt.gradient(dt)                           # Compute the Gradient
freqs, power = filt.psd(az, len(az), 50)           # Power Spectral Density
bl, al = filt.create_filter(3, 1, "lowpass", fs)   # Low-pass Filter Design
lp = filt.filter(bl, al, dt)                       # Low-pass Filter Signal
count, peaks = filt.count_peaks(lp, t_low, t_high) # Find & Count the Peaks

# Plot the results
plt.plot(t, lp)
plt.title("Detected Peaks = %d" % count)
plt.plot(t[peaks], lp[peaks], 'rx')
plt.plot(t, [t_low]*len(lp), "b--")
plt.plot(t, [t_high]*len(lp), "b--")
plt.show()

