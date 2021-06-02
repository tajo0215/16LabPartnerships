#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:18:55 2021

@author: jun
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time, time_ns
import numpy as np


class IdleDetector():

    num_samples = 0
    refresh_time = 0
    N = 0

    __times = None
    __ax = None
    __ay = None
    __az = None

    __average_x = None
    __delta_x = None
    __L2 = None
    __L1 = None
    __L_inf = None

    __comms = None

    figure, axis = 0, 0

    idle = False
    idle_time_previous = 0
    active_time = 0

    previous_time = 0

    def __init__(self, num_samples, refresh_time, N, com_port, baud_rate):
        self.num_samples = num_samples
        self.refresh_time = refresh_time
        self.N = N

        self.__times = CircularList([], self.num_samples)
        self.__ax = CircularList([], self.num_samples)
        self.__ay = CircularList([], self.num_samples)
        self.__az = CircularList([], self.num_samples)

        self.__average_x = CircularList([], self.num_samples)
        self.__delta_x = CircularList([], self.num_samples)
        self.__L2 = CircularList([], self.num_samples)
        self.__L1 = CircularList([], self.num_samples)
        self.__L_inf = CircularList([], self.num_samples)

        #self.__comms = Communication(com_port, baud_rate=baud_rate)

        self.figure, self.axis = plt.subplots(2, 2)

        self.idle = False
        self.idle_time_previous = 0
        self.active_time = 0

        self.previous_time = 0

    """
    Helper function for plotting data
    return: Displays 4 plots: ax, ay, az, and L-infinity 
    """
    def plotData(self):
        current_time = time()
        if (current_time - self.previous_time > self.refresh_time):
            self.previous_time = current_time

            plt.cla()

            self.axis[0, 0].cla()
            self.axis[0, 0].plot(self.__ax)
            self.axis[0, 0].set_title("X Values")

            self.axis[0, 1].cla()
            self.axis[0, 1].plot(self.__ay)
            self.axis[0, 1].set_title('Y Values')

            self.axis[1, 0].cla()
            self.axis[1, 0].plot(self.__az)
            self.axis[1, 0].set_title('Z Values')

            self.axis[1, 1].cla()
            self.axis[1, 1].plot(self.__L_inf)
            self.axis[1, 1].set_title("L-infinite Values")

            plt.show(block=False)
            plt.pause(0.001)

    """
    Helper function to detect an idle
    Sends a message to the Arduino on which state it is in
    returns: Nothing 
    """  
    def detectIdle(self, point):
        if time() - self.idle_time_previous >= 5:
            self.idle_time_previous = time()
            if point > 2427 + 100 or point < 2427 - 100:
                self.idle = False
            else:
                self.idle = True
                self.__comms.send_message("Idle State")
        if self.idle and time() - self.active_time >= 1:
            self.active_time = time()
            if point > 2427 + 100 or point < 2427 - 100: 
                self.idle = False
                self.idle_time_previous = time()
                self.__comms.send_message("Active State")
            else:
                self.idle = True

    """
    Adding detectIdleWearable for Lab 7 Challenge 3
    """
    def detectIdleWearable(self, point):
        if time() - self.idle_time_previous >= 5:
            self.idle_time_previous = time()
            if point > 2427 + 100 or point < 2427 - 100:
                self.idle = False
                return False
            else:
                self.idle = True
                return True
        if self.idle and time() - self.active_time >= 1:
            self.active_time = time()
            if point > 2427 + 100 or point < 2427 - 100: 
                self.idle = False
                self.idle_time_previous = time()
                return False
            else:
                self.idle = True
                return True

    """ 
    Main Function that runs everything
    The function will get data from the ESP32, add it to all the variables and lists, graph if wanted, and
    get the idle state.
    
    returns: Nothing
    """
    def run(self, graph_data):

        self.__comms.clear() # clearing comms
        self.__comms.send_message("Sending Data") #sending message to signify data transfer should begin

        try:
            average_previous_time = 0 # used for average_x values
            avg_cycles = 0 # used for average_x values
            while(True):
                message = self.__comms.receive_message()
                if(message != None):
                    try:
                        (m1, m2, m3, m4) = message.split(',')
                    except ValueError:        # if corrupted data, skip the sample
                        continue
                    # add the new values to the circular lists
                    self.__times.add(int(m1))
                    self.__ax.add(int(m2))
                    self.__ay.add(int(m3))
                    self.__az.add(int(m4))

                    # computing the various transformations and adding the data to corresponding lists 
                    if(time() - average_previous_time > self.N):
                        average_previous_time = time()
                        self.__average_x.add(np.average(self.__ax))
                        if avg_cycles < 5 and self.N < .32:
                            self.N *= 2
                    self.__delta_x.add(np.absolute(self.__ax[len(self.__ax) - 1] - self.__ax[len(self.__ax) - 2])) 
                    self.__L2.add(np.linalg.norm([int(m2), int(m3), int(m4)]))
                    self.__L1.add(np.absolute(int(m2)) +
                                  np.absolute(int(m3)) + np.absolute(int(m4)))
                    self.__L_inf.add(np.max([int(m2), int(m3), int(m4)]))

                    # if we want to graph the data, it will do so here
                    if graph_data:
                        self.plotData(self.previous_time)

                    point = self.__L_inf[len(self.__L_inf) - 1] # gets the last L-Inf value
                    self.detectIdle(point) # computes the idle state

        except(Exception, KeyboardInterrupt) as e:
            print(e)                     # Exiting the program due to exception
        finally:
            self.__comms.send_message("Sleep Mode")  # stop sending data
            self.__comms.close()
