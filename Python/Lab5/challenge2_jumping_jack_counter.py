from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
import numpy as np

if __name__ == "__main__":
    fs = 50                         # sampling rate
    num_samples = 250               # 5 seconds of data @ 50Hz
    process_time = 1                # compute the step count every second

    times = CircularList([], num_samples)
    ax = CircularList([], num_samples)
    ay = CircularList([], num_samples)
    az = CircularList([], num_samples)

    ped = Pedometer(num_samples, fs, [])

    comms = Communication("COM5", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    try:
        while(True):
            message = comms.receive_message(num_bytes=3000)
            if(message != None):
                try:
                    tempData = message.split(",")
                    length = int(len(tempData) / 4)
                    idx = 0
                    for i in range(length):
                        times.add(int(tempData[idx]))
                        ax.add(int(tempData[idx+1]))
                        ay.add(int(tempData[idx+2]))
                        az.add(int(tempData[idx+3]))
                        idx += 4
                except ValueError:        # if corrupted data, skip the sample
                    continue
                
                for i in range(len(ax)):
                    ped.add(ax[i], ay[i], az[i])

                steps, peaks, filtered = ped.process()
                comms.send_message(f'Count{steps}')
    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
