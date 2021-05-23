"""
Lab 7 Challenge 2: GMM HR Monitor

@author: Jun Park (A15745118)
"""

import glob

import numpy as np
import ECE16Lib.DSP as filt

from ECE16Lib.Communication import Communication
from ECE16Lib.HRMonitor import HRMonitor
from sklearn.mixture import GaussianMixture as GMM
from matplotlib import pyplot as plt
from time import sleep
from time import time
from sys import exit

# Retrieve a list of the names of the subjects
def get_subjects(directory):
    filepaths = glob.glob(directory + "\\*")
    return [filepath.split("\\")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
    search_key = "%s\\%s\\%s_%02d_*.csv" % (directory, subject, subject, trial)
    filepath = glob.glob(search_key)[0]
    t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
    t = (t-t[0])/1e3
    hr = get_hr(filepath, len(ppg), fs)

    fs_est = estimate_fs(t)
    #if(fs_est < fs-1 or fs_est > fs):
        #print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est, filepath))

    return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
    count = int(filepath.split("_")[-1].split(".")[0])
    seconds = num_samples / fs
    return count / seconds * 60  # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
    return 1 / np.mean(np.diff(times))

if __name__ == "__main__":
    fs = 50
    num_samples = 500
    process_time = 1
    
    directory = ".\\data"
    subjects = get_subjects(directory)
    
    hr_monitor = HRMonitor(num_samples, fs, [])
    
    input("First, the GMM training begins. Press [ENTER] to begin.\n")
    gmm = hr_monitor.train(directory, subjects)
    
    comms = Communication("COM5", 115200)
    comms.clear()
    input("Ready to collect data? Press [ENTER] to begin.\n")
    print("Start measruing in...")
    for k in range(3,0,-1):
        print(k)
        sleep(1)
    print("Begin!")
    
    comms.send_message("wearable")
    
    try:
        previous_time = time()
        
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4, m5) = message.split(",")
                except Exception as e:
                    print(e)
                    print("Corrupted data. Skipping sample: {}".format(message))
                    continue
                
                hr_monitor.add(int(m1)/1e3, int(m5))
                
                current_time = time()
                if (current_time - previous_time > process_time):
                    previous_time = current_time
                    
                    hr_tested, peaks = hr_monitor.predict(gmm)
                    msg = "HR{:f}".format(hr_tested)
                    print(msg)
                    comms.send_message(msg)
                    
    except(KeyboardInterrupt) as e:
        print(e)
    finally:
        print("Closing connection.")
        comms.send_message("sleep")
        sleep(3)
        comms.close()
        exit()
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    