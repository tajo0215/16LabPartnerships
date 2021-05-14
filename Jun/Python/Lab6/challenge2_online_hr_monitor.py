"""
Lab 6 Challenge 2: Online Heart Rate Monitor

@author: Jun Park (A15745118)
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import sleep
from time import time
import numpy as np

if __name__ == "__main__":
    fs = 50
    num_samples = 500
    process_time = 1
    
    hr_monitor = HRMonitor(num_samples, fs, [])
    
    comms = Communication("/dev/cu.usbmodem142101", 115200)
    comms.clear()
    input("Ready to collect data? Press [ENTER] to begin.\n")
    print("Start measuring in...")
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
                    (m1, _, _, _, m2) = message.split(",")
                except ValueError:
                    continue
                
                hr_monitor.add(int(m1)/1e3, int(m2))
                
                current_time = time()
                if (current_time - previous_time > process_time):
                    previous_time = current_time
                    
                    hr, peaks, filtered = hr_monitor.process()
                    #hr_msg = "HR: {:f}".format(hr)
                    #print(hr_msg)
                    comms.send_message(f'HR{hr}')
                    
                    plt.cla()
                    plt.plot(filtered)
                    plt.title("HR Count: %f" % hr)
                    plt.show(block=False)
                    plt.pause(0.001)
    except(KeyboardInterrupt) as e:
        print(e)
    finally:
        print("Closing connection.")
        comms.send_message("sleep")
        comms.close()
                    
