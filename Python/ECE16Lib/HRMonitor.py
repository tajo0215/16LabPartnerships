"""
ECE 16 Lib HRMonitor.py

@author: Jun Park (A15745118)
"""

from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np
import matplotlib.pyplot as plt
import glob

from sklearn.mixture import GaussianMixture as GMM
from scipy.stats import norm

"""
A class to enable a simple heart rate monitor
"""
class HRMonitor:
    """
    Encapsulated class attributes (with default values)
    """
    __hr = 0           # the current heart rate
    __time = None      # CircularList containing the time vector
    __ppg = None       # CircularList containing the raw signal
    __filtered = None  # CircularList containing filtered signal
    __num_samples = 0  # The length of data maintained
    __new_samples = 0  # How many new samples exist to process
    __fs = 0           # Sampling rate in Hz
    __thresh = 0.6     # Threshold from Tutorial 2
    
    """
    Initialize the class instance
    """
    def __init__(self, num_samples, fs, times=[], data=[]):
        self.__hr = 0
        self.__num_samples = num_samples
        self.__fs = fs
        self.__time = CircularList(data, num_samples)
        self.__ppg = CircularList(data, num_samples)
        self.__filtered = CircularList([], num_samples)
        
    """
    Add new samples to the data buffer
    Handles both integers and vectors!
    """
    def add(self, t, x):
        if isinstance(t, np.ndarray):
            t = t.tolist()
        if isinstance(x, np.ndarray):
            x = x.tolist()

        if isinstance(x, int):
            self.__new_samples += 1
        else:
            self.__new_samples += len(x)

        self.__time.add(t)
        self.__ppg.add(x)

    """
    Compute the average heart rate over the peaks
    """
    def compute_heart_rate(self, peaks):
        t = np.array(self.__time)
        
        return 60 / np.mean(np.diff(t[peaks]))

    """
    Process the new data to update step count
    """
    def process(self):
        # Grab only the new samples into a NumPy array
        x = np.array(self.__ppg[ -self.__new_samples: ])
        
        # Filter the signal (feel free to customize!)
        x = filt.detrend(x, 10)
        x = filt.moving_average(x, 50)
        x = filt.gradient(x)
        x = filt.normalize(x)

        # Store the filtered data
        self.__filtered.add(x.tolist())
        
        # Find the peaks in the filtered data
        _, peaks = filt.count_peaks(self.__filtered, self.__thresh, 1)
        
        # Update the step count and reset the new sample count
        self.__hr = self.compute_heart_rate(peaks)
        self.__new_samples = 0
        
        # Return the heart rate, peak locations, and filtered data
        return self.__hr, peaks, np.array(self.__filtered)
    
    
    def train(self, directory, subjects):
        
        print("Training All Data")
        train_data = np.array([])
        
        for subject in subjects:
            for trial in range(1,11):
                
                search_key = "%s\\%s\\%s_%02d_*.csv" % (directory, subject, subject, trial)
                filepath = glob.glob(search_key)[0]
                t, ppg = np.loadtxt(filepath, delimiter=",", unpack=True)
                t = (t-t[0])/1e3
                
                num_samples = len(ppg)
                
                count = int(filepath.split("_")[-1].split(".")[0])
                seconds = num_samples / self.__fs
                hr_trained = count / seconds * 60
                
                fs_est = 1 / np.mean(np.diff(t))
                
                ppg = filt.detrend(ppg, 25)
                ppg = filt.moving_average(ppg, 5)
                ppg = filt.gradient(ppg)
                ppg = filt.normalize(ppg)
                
                train_data = np.append(train_data, ppg)
                
        train_data = train_data.reshape(-1,1)
        gmm = GMM(n_components=2).fit(train_data)
        
        plt.hist(train_data, 100, density=True)
        
        weight_0 = float(gmm.weights_[0])
        mu_0 = float(gmm.means_[0])
        var_0 = float(gmm.covariances_[0])

        x_0 = np.linspace(0, 1)
        y_0 = weight_0 * norm.pdf(x_0, mu_0, np.sqrt(var_0))
        plt.plot(x_0, y_0)
        
        weight_1 = float(gmm.weights_[1])
        mu_1 = float(gmm.means_[1])
        var_1 = float(gmm.covariances_[1])

        x_1 = np.linspace(0, 1)
        y_1 = weight_1 * norm.pdf(x_1, mu_1, np.sqrt(var_1))
        plt.plot(x_1, y_1)

        plt.show()
        
        return gmm
    
    
    def predict(self, gmm):
        
        x = np.array(self.__ppg[ -self.__new_samples: ])
        
        x = filt.detrend(x, 10)
        x = filt.moving_average(x, 50)
        x = filt.gradient(x)
        x = filt.normalize(x)
        
        test_data = x
        
        labels = gmm.predict(test_data.reshape(-1,1))
        num_samples = len(x)
        
        peaks = np.diff(labels, prepend=0) == 1
        count = sum(peaks)
        seconds = num_samples / self.__fs
        
        hr_tested = count / seconds * 60 
           
        return hr_tested, peaks

    """
    Clear the data buffers and step count
    """
    def reset(self):
        self.__hr = 0
        self.__time.clear()
        self.__ppg.clear()
        self.__filtered.clear()
          