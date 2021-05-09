from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
import numpy as np

# Save data to file
def save_data(filename, data):
    np.savetxt(filename, data, delimiter=",")

# Load data from file
def load_data(filename):
    return np.genfromtxt(filename, delimiter=",")


def getData():
    times = CircularList([], num_samples)
    ax = CircularList([], num_samples)
    ay = CircularList([], num_samples)
    az = CircularList([], num_samples)
    message = comms.receive_message()
    while message != None:
        (m1, m2, m3, m4) = message.split(",")
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        message = comms.receive_message()
    data = np.column_stack([times, ax, ay, az])
    save_data("./data/jumpingData.csv", data)

def run():
    data = load_data("./data/jumpingData.csv")
    fs = 100
    num_samples = 200
    process_time = 1
    row_idx = 0
    
    ped = Pedometer(num_samples, fs, [])

    try:
        previous_time = time()
        while(True):
            m1 = data[row_idx:,0]
            m2 = data[row_idx:,1]
            m3 = data[row_idx:,2]
            m4 = data[row_idx:,3]
            
            # Collect data in the pedometer
            ped.add(m2, m3, m4)

            # if enough time has elapsed, process the data and plot it
            current_time = time()
            if (current_time - previous_time > process_time):
                previous_time = current_time

                steps, peaks, filtered = ped.process()
                comms.send_message(f'Count{steps}')
    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
    

if __name__ == "__main__":

    comms = Communication("COM5", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if(message == "s"):
                try:
                    print("done 1")
                    getData()
                    print("done 2")
                    run()
                    print("done 3")
                except ValueError:        # if corrupted data, skip the sample
                    continue
    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
