"""
Lab 5 Challenge 1: challenge1_online_pedometer.py

@author: Jun Park (A15745118)
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.Pedometer import Pedometer
#from matplotlib import pyplot as plt
from time import sleep
from time import time
#import numpy as np

if __name__ == "__main__":
    fs = 50                         # sampling rate
    num_samples = 250               # 5 seconds of data @ 50Hz
    process_time = 1                # compute the step count every second

    ped = Pedometer(num_samples, fs, [])

    #comms = Communication("/dev/cu.SLAB_USBtoUART", 115200)
    comms = Communication("/dev/cu.zzangu-ESP32_SPP_SERVER", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    input("Ready to collect data? Press [ENTER] to begin.\n")
    sleep(3)
    comms.send_message("wearable")  # begin sending data

    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4) = message.split(",")
                except ValueError:        # if corrupted data, skip the sample
                    continue

                # Collect data in the pedometer
                ped.add(int(m2), int(m3), int(m4))

                # if enough time has elapsed, process the data and plot it
                current_time = time()
                if (current_time - previous_time > process_time):
                    previous_time = current_time

                    steps, peaks, filtered = ped.process()
                    comms.send_message(f'Walks{steps}')
                    
                    # plt.cla()
                    # plt.plot(filtered)
                    # plt.title("Step Count: %d" % steps)
                    # plt.show(block=False)
                    # plt.pause(0.001)
                    
    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()

