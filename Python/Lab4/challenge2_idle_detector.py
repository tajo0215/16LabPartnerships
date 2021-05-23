from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np


"""
If the value is 100 greater than 2427 or 100 less, then it returns true to represent active state
"""
def checkIdle(value):
    return value > 2427 + 100 or value < 2427 - 100


if __name__ == "__main__":
    num_samples = 250               # 5 seconds of data @ 50Hz
    refresh_time = 0.25            # update the plot every 0.1s (10 FPS)
    N = .04

    times = CircularList([], num_samples)
    ax = CircularList([], num_samples)
    ay = CircularList([], num_samples)
    az = CircularList([], num_samples)

    L_inf = CircularList([], num_samples)


    comms = Communication("COM5", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("Sending Data")  # begin sending data


    idle = False
    idle_time_previous = 0
    active_time = 0

    try:
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError:        # if corrupted data, skip the sample
                    continue

                # add the new values to the circular lists
                times.add(int(m1))
                ax.add(int(m2))
                ay.add(int(m3))
                az.add(int(m4))

                L_inf.add(np.max([int(m2), int(m3), int(m4)])) # choosing L infinite because it will return the largest value which indicates largest change
                
                point = L_inf[len(L_inf) - 1] # getting the current data point from L_inf

                if time() - idle_time_previous >= 5: # checking if 5 seconds has passed for the Idle State
                    idle_time_previous = time() 
                    if checkIdle(point): # checks if our point is above the thresholds to be considered active
                        idle = False
                    else:
                        idle = True
                        comms.send_message("Idle State")
                if idle and time() - active_time >= 1: # checking if 1 second has passed for the Active State
                    active_time = time()
                    if checkIdle(point): 
                        idle = False
                        idle_time_previous = time()
                        comms.send_message("Active State")
                    else:
                        idle = True

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        comms.send_message("Sleep Mode")  # stop sending data
        comms.close()
