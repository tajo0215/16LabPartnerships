from ECE16Lib.CircularList import CircularList
import glob
import numpy as np
from ECE16Lib.Communication import Communication
from matplotlib import pyplot as plt
from ECE16Lib.HRMonitor import HRMonitor
from time import sleep
from time import time
import pickle 


if __name__ == "__main__":
    fs = 50
    num_samples = 500
    process_time = 1.5
    
    directory = ".\\data"
    
    hr_monitor = HRMonitor(num_samples, fs, [])

    comms = Communication("COM5", 115200)
    comms.clear()
    comms.send_message('wearable')

    user_input = input("Would you like to train the model? [Y/N]")

    if user_input == "Y":
        hr_monitor.train(directory)

    times = CircularList([], num_samples)
    ppg = CircularList([], num_samples)
    
    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2) = message.split(",") #splits the data: time, ax, ay, az, ppg, HR
                except Exception as e:        # if corrupted data, skip the sample
                    print(e)
                    print("Corrupted data. Skipping sample: {}".format(message))
                    continue

                times.add(int(m1))
                ppg.add(int(m2))
                
                current_time = time()
                if (current_time - previous_time > process_time):
                    previous_time = current_time

                    data = np.column_stack([times, ppg])

                    np.savetxt("./data/testdata.csv", data, delimiter=",")

                    hr = hr_monitor.predict("./data/testdata.csv")

                    comms.send_message(f"HR{hr:.2f}")
                    print(hr)

    except(KeyboardInterrupt) as e:
        print(e)
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()

    






        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    