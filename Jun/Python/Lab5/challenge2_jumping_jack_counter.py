"""
Lab 5 Challenge 2: Jumping Jack Counter

@author: Jun Park (A15745118)
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
#from matplotlib import pyplot as plt
from time import sleep

if __name__ == "__main__":
    
    fs = 50                 # smpling rate at 50Hz
    num_samples = 250       # 5 seconds of data @50Hz
    process_time = 1        # compute the jumping count every second
    
    # Adding CircularList to keep updating incoming data
    times = CircularList([], num_samples)
    ax = CircularList([], num_samples)
    ay = CircularList([], num_samples)
    az = CircularList([], num_samples)

    ped = Pedometer(num_samples, fs, [])

    comms = Communication("/dev/cu.zzangu-ESP32_SPP_SERVER", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    input("Ready to collect data? Press [ENTER] to begin.\n")
    sleep(3)
    comms.send_message("wearable")  # begin sending data

    try:
        while(True):
            # receive a message with enough space of bytes
            message = comms.receive_message(num_bytes=3000)
            
            if(message != None):
                
                try:
                    tempData = message.split(",")
                    # length is for determining how many data we received
                    length = int(len(tempData) / 4)
                    idx = 0
                    # Every 4 data points, we store each data as time, ax, ay, and az
                    for i in range(length):
                        times.add(int(tempData[idx]))
                        ax.add(int(tempData[idx+1]))
                        ay.add(int(tempData[idx+2]))
                        az.add(int(tempData[idx+3]))
                        idx += 4
                except ValueError:        # if corrupted data, skip the sample
                    continue
                
                # Once finish storing, begin process loop
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
    

    

    
            