"""
Lab 5 Challenge 2: Jumping Jack Counter

@author: Jun Park (A15745118)
"""

from ECE16Lib.Communication import Communication
#from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
#from matplotlib import pyplot as plt
from time import time
from time import sleep
import numpy as np

def save_data(filename, data):
    np.savetxt(filename, data, delimiter=",")
    
def load_data(filename):
    return np.genfromtxt(filename, delimiter=",")

def collect_jumping_jack():
    
    num_samples = 500
    fs = 50
    process_time = 1

    ped = Pedometer(num_samples, fs, [])    
    
    comms = Communication("/dev/cu.zzangu-ESP32_SPP_SERVER", 115200)
    
    try:
        previous_time = time()
        comms.clear()                   # just in case any junk is in the pipes
        input("Ready to collect data? Press [ENTER] to begin.\n")
        sleep(3)
        comms.send_message("wearable")  # begin sending data
        
        sample = 0
        while(sample < num_samples):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4) = message.split(",")
                except ValueError:
                    continue
                
                ped.add(int(m2), int(m3), int(m4))
                
                current_time = time()
                if(current_time - previous_time > process_time):
                    previous_time = current_time
                    
                    jumps, peaks, filtered = ped.process()
                    comms.send_message(f'Jumps{jumps}')
                    
        #data = np.column_stack([jumps, peaks, filtered])
        
    except(Exception, KeyboardInterrupt) as e:
        print(e)
        
    finally:
        print("Closing connection.")
        comms.send_message("sleep")
        comms.close()

    # return data

if __name__ == "__main__":
    
    
    collect_jumping_jack()
    
    
    """
    I was trying to use functions of saving and loading file, but I'm not too sure about it,
    so I commented out :(
    """
    # filename = "./data/jumpingjack.csv"
    
    # data = collect_jumping_jack()
    # save_data(filename, data)
    
    # data = load_data(filename)
    
    # process_time = 1
    # previous_time = ()
    
    # while(True):
        
    #     current_time = time()
    #     if (current_time- previous_time > process_time):
    #         previous_time = current_time
            
    #         steps, peaks, filtered = ped.process()
    
    

    

    
            