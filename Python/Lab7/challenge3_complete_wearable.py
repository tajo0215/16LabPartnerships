from ECE16Lib.Communication import Communication
from ECE16Lib.Pedometer import Pedometer
from ECE16Lib.HRMonitor import HRMonitor

import numpy as np 
import time
from pyowm import OWM
import datetime


"""
Wearable Overview
    1. Weather/Time - Updates Every second and is always displayed
    2. If button pressed, get HR for next 20 seconds
    3. If button held, reset Pedometer and buzz motor for 1 second
    4. Pedometer is on always
"""


def updateWeather(ser, weather):
    curr_time = time.localtime() # gets the local time at Walnut Creek, CA PST Time
    curr_time = time.strftime("%H:%M:%S") # changes the format of the time to hour:minutes:seconds
    curr_date = str(datetime.date.today()) # gets the date and converts it to a string
    
    #output formatting: Time: XX:XX:XX \n Date: XXXX-XX-XX \n SF Temp(F): XX
    msg = f"Time: {curr_time},Date: {curr_date},SF Temp(F): {str(int(weather.temperature('fahrenheit')['feels_like']))}"
    return msg


if __name__ == "__main__":

    owm = OWM('0bd12c8321fffb6b6684a1e2a83236fd').weather_manager() # gets the weather manager using my API key
    weather = owm.weather_at_place('San Francisco, CA, US').weather # gets the weather data at San Francisco, CA 

    fs = 50                         # sampling rate
    num_samples = 250               # 5 seconds of data @ 50Hz
    process_time = 1                # compute the step count every second

    ped = Pedometer(num_samples, fs, [])
    hr_monitor = HRMonitor(num_samples, fs, [])

    comms = Communication("COM5", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    print("Starting in: ")
    for k in range(3,0,-1):
        print(k)
        time.sleep(1)

    try:
        previous_time = time.time()
        
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4, m5, hr_cmd) = message.split(",") #splits the data: time, ax, ay, az, ppg, HR
                except Exception as e:        # if corrupted data, skip the sample
                    print(e)
                    print("Corrupted data. Skipping sample: {}".format(message))
                    continue
                
                if hr_cmd == "HR":
                    hr_monitor.add(int(m1)/1e3, int(m5)) # adds the time and ppg data
                

                ped.add(int(m2), int(m3), int(m4))
                
                current_time = time.time()
                if (current_time - previous_time > process_time):
                    previous_time = current_time

                    weather_time_msg = updateWeather(comms, weather)

                    if hr_cmd == "HR":
                        hr, peaks, filtered = hr_monitor.process() # process the data
                        hr_msg = f'{hr:.2f}'# format the message to 2 decimal places
                    else:
                        hr_msg = "NULL"

                    steps, peaks, filtered = ped.process() #procceses data

                    msg = f"D:{weather_time_msg};{hr_msg};{steps}"
                    comms.send_message(msg)

                    print(msg)
    except(KeyboardInterrupt) as e:
        print(e)
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
