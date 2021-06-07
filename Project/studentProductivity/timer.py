import threading
from time import sleep
from datetime import datetime
from ECE16Lib.Communication import Communication

class Timer:

    def __init__(self, port, baud_rate):

        self.__working_duration = 30 * 60
        self.__break_duration = 15 * 60
        self.__reset_signal = False
        self.__pause_signal = False
        self.__ask_termination = False
        self.__termination_signal = False

        self.__comms = Communication(port, baud_rate)
        self.__comms.setup()

    def start(self):

        self.__comms.clear() 
        # display current date time.
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("Date Time Now: ", dt_string)
        print("-" * 60)

        self.__comms.send_message("Timer Ready")

        while(True):
            message = self.__comms.receive_message()
            if(message != None):
                try:
                    m1 = message 
                except Exception as e:        # if corrupted data, skip the sample
                    print(e)
                    print("Corrupted data. Skipping sample: {}".format(message))
                    continue

                if "start" in m1:
                    self.__comms.send_message("Timer Started")

                    threading.Thread(target=self.__get_user_input).start()
                    threading.Thread(target=self.main_loop).start()
                    
                elif "pause" in m1:
                    self.pause()
                elif "continue" in m1:
                    self.__pause_signal = False
                elif "restart" in m1:
                    self.reset()

    def main_loop(self):

        while 1:

            # Initialize
            self.__reset_signal = False
            self.__pause_signal = False
            self.__ask_termination = False

            # Focus Time
            print("Focus Time! Timer (30 minutes) is running.\n")

            # Change this value for easy debug.
            a_second = 1

            for i in range(1, self.__working_duration + 1):

                sleep(a_second)

                # Handle signal - reset has higher priority than pause.
                if self.__reset_signal is True:
                    break

                # Wait until pause_signal is false.
                while self.__pause_signal is True:
                    sleep(0.01)

                # Print information
                if i == self.__working_duration:
                    pass       # Display nothing in this case.

                elif i % (5 * 60) == 0:
                    print(f"Time: {(i / 60)} minutes ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")

                elif i == self.__working_duration - 60:
                    print(f"Time: 1 minute left! ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")

            if self.__reset_signal is True:
                continue

            # Break Time
            print("-" * 60)
            print("Break Time! Timer (15 minutes) is running.\n")
            for i in range(1, self.__break_duration + 1):

                sleep(a_second)

                # Handle signal - reset has higher priority than pause.
                if self.__reset_signal is True:
                    break

                # Wait until pause_signal is false.
                while self.__pause_signal is True:
                    sleep(0.01)

                # Print information
                if i == self.__break_duration:
                    pass  # Display nothing in this case.
                elif i == self.__break_duration - 1 * 60:
                    print(f"Time: 1 minute left! ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")
                elif i % (5 * 60) == 0:
                    print(f"Time: {(i / 60)} minutes ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")

            # Complete one cycle.
            if self.__reset_signal is False:
                print("-" * 60)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print("Date Time Now: ", dt_string)
                self.__ask_termination = True

                print("1. Press 'r' to restart the current timer.\n"
                      "2. Press 't' to terminate program.\n")

                while self.__reset_signal is False and self.__termination_signal is False:
                    sleep(0.01)

                if self.__termination_signal is True:
                    print("-" * 60)
                    print("Exit Program.")
                    return
                else:
                    self.__ask_termination = False
                    print("-" * 60)
                    print("1. Press 'r' to reset/restart the current timer.\n"
                          "2. Press 'p' to pause/unpause the current timer.\n")
                    threading.Thread(target=self.__get_user_input).start()

    def __get_user_input(self):

        while 1:

            value = input()

            if value == 'r':
                self.__reset_signal = True
                print(f"Reset Timer. ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")
                print("-" * 60)

            elif value == 'p':
                self.__pause_signal = not self.__pause_signal
                print(f"Timer {'paused.' if self.__pause_signal is True else 'start.'} ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")
                print("-" * 60)

            elif self.__ask_termination and value == 't':
                self.__termination_signal = True
                return

    def reset(self):
        self.__reset_signal = True

    def pause(self):
        self.__pause_signal = True
