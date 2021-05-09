"""
Lab 5 Tutorial 3: tutorial_pedometer.py

@author: Jun Park (A15745118)
"""

from ECE16Lib.Pedometer import Pedometer
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    return np.genfromtxt(filename, delimiter=",")

# Load the data as a 500x4 ndarray
data = load_data("./data/8steps_10s_50hz.csv")
t = data[:,0]
t = (t - t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]

# Test the Pedometer with offline data
ped = Pedometer(500, 50, [])
ped.add(ax, ay, az)
steps, peaks, filtered = ped.process()

# Plot the results
plt.plot(t, filtered)
plt.title("Detected Peaks = %d" % steps)
plt.plot(t[peaks], filtered[peaks], 'rx')
plt.plot(t, [25]*len(filtered), "b--")
plt.plot(t, [100]*len(filtered), "b--")
plt.show()
