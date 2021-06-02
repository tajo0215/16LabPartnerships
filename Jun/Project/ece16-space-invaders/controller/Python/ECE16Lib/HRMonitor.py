"""
ECE 16 Lib HRMonitor.py

@author: Jun Park (A15745118)
"""

from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np
import matplotlib.pyplot as plt
import glob
import pickle

from scipy.stats.stats import pearsonr
from sklearn.mixture import GaussianMixture as GMM
from sklearn.metrics import mean_squared_error as MSE
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
    
    
  def get_hr(self, filepath):
    count = int(filepath.split("_")[-1].split(".")[0])
    seconds = self.__num_samples / self.__fs
    return count / seconds * 60
    
  def get_data(self, directory, subject, trial):
    search_key = "%s\\%s\\%s_%02d_*.csv" % (directory, subject, subject, trial)
    filepath = glob.glob(search_key)[0]
    t, ppg = np.loadtxt(filepath, delimiter=",", unpack=True)
    t = (t-t[0])/1e3
    hr = self.get_hr(filepath)

    fs_est = 1 / np.mean(np.diff(t))

    return t, ppg, hr, fs_est
    
  def estimate_hr(self, labels):
    peaks = np.diff(labels, prepend=0) == 1
    count = sum(peaks)
    seconds = self.__num_samples / self.__fs
    hr = count / seconds * 60
    return hr, peaks
    
  def estimate_hr_test(self, labels, num_samples):
    peaks = np.diff(labels, prepend=0) == 1
    count = sum(peaks)
    seconds = num_samples / self.__fs
    hr = count / seconds * 60
    return hr, peaks
    
  def train(self, directory):
     
    model = GMM(n_components = 2)
       
    filepaths = glob.glob(directory + "\\*")
    subjects = [filepath.split("\\")[-1] for filepath in filepaths]
        
    print("Training Data...\n")
        
    for current in subjects:
                
      y_pred = []  # Prediction
      y_true = []  # Actual
                
      train_data = np.array([])
      valid_data = np.array([])
                
      # Training All the Data excluding current subject
      for subject in subjects:
        for trial in range(1, 11):
          t, ppg, hr, fs_est = self.get_data(directory, subject, trial)
                        
          if subject != current:
            ppg = filt.detrend(ppg, 25)
            ppg = filt.moving_average(ppg, 5)
            ppg = filt.gradient(ppg)
            ppg = filt.normalize(ppg)
                            
            train_data = np.append(train_data, ppg)
                
      train_data = train_data.reshape(-1,1)
      model.fit(train_data)
                
      # Get Heart Rate of the current subject
      for trial in range(1, 11):
        t, ppg, hr, fs_est = self.get_data(directory, current, trial)
                   
        y_true.append(hr)
                    
        ppg = filt.detrend(ppg, 25)
        ppg = filt.moving_average(ppg, 5)
        ppg = filt.gradient(ppg)
        ppg = filt.normalize(ppg)
                    
        valid_data = np.append(valid_data, ppg)
                    
        labels = model.predict(valid_data.reshape(-1,1))
                    
        hr_est, peaks = self.estimate_hr(labels)
                    
        y_pred.append(hr_est)
                
      rmse = np.sqrt(MSE(y_true, y_pred))
      r = pearsonr(y_true, y_pred)[0]
                
      print(f"Student({current}): RMSE = {rmse:.4f}, r = {r:.4f}")
                
    print("\n" + "-"*40 + "\n")
            
    print("Training Complete")
    pickle.dump(model, open("GMMModel.sav", 'wb'))
    

  def predict(self, filename):
        
    model = pickle.load(open("GMMModel.sav", 'rb'))
        
    data = np.genfromtxt(filename, delimiter=',')
        
    t = data[:,0]
    t = (t-t[0]) / 1e3
    ppg = data[:,1]
        
    ppg = filt.detrend(ppg,25)
    ppg = filt.moving_average(ppg, 5)
    ppg = filt.gradient(ppg)
    ppg = filt.normalize(ppg)
        
    labels = model.predict(ppg.reshape(-1,1))
        
    hr_est, peaks = self.estimate_hr_test(labels, len(ppg))
        
    return hr_est

  """
  Clear the data buffers and step count
  """
  def reset(self):
    self.__hr = 0
    self.__time.clear()
    self.__ppg.clear()
    self.__filtered.clear()
          