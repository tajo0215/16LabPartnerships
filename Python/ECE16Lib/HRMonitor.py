from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np

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
        x = np.array(self.__ppg[-self.__new_samples:])

        # Filter the signal (feel free to customize!)
        x = filt.detrend(x, 25)
        x = filt.moving_average(x, 4)
        x = filt.gradient(x)
        x = filt.normalize(x)

        # Store the filtered data
        self.__filtered.add(x.tolist())

        # Find the peaks in the filtered data
        _, peaks = filt.count_peaks(x, self.__thresh, 1)

        # Update the step count and reset the new sample count
        self.__hr = self.compute_heart_rate(peaks)
        self.__new_samples = 0

        # Return the heart rate, peak locations, and filtered data
        return self.__hr, peaks, np.array(self.__filtered)

    """
  Clear the data buffers and step count
  """

    def reset(self):
        self.__hr = 0
        self.__time.clear()
        self.__ppg.clear()
        self.__filtered.clear()
