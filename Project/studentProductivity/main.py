from ECE16Lib.Communication import Communication
from student_productivity import StudentCalender, Pomodoro, HabitTracker
import time
import datetime

def main():

    calender = StudentCalender()
    habitTracker = HabitTracker()
    pomodoro_timer = Pomodoro()

    comms = Communication("COM5", 115200)
    comms.clear()


    # asks for any  new habits to be added 
    if input("Would you like to add habits today? Y/N: ") == "Y":
        (name, habit_time) = input("Please input your habit: Habit Name, Habit Time (XX:XX PM/AM Format): ").split(',')
        habitTracker.addHabit(name, habit_time)

        # keeps asking until the user types N
        while True:
            if input("Would you like to add another habit? Y/N: ") == "Y":
                (name, habit_time) = input("Please input your habit: Habit Name, Habit Time (XX:XX PM/AM Format): ").split(',')
                habitTracker.addHabit(name, habit_time)
            else:
                break
    
    # orders the habits in order of increasing time throughout the day 
    habitTracker.orderHabits()

    # used to store time values 
    habit_time = 0
    event_time = 0
    timer_time = 0

    timer_on = False

    comms.send_message('Timer Ready')

    while True:


        # if the 30 seconds has passed, we check the habit tracker again 
        if time.time() - habit_time >= 30:
            habit_time = time.time()

            msg = habitTracker.checkHabits()

            # if the msg is None, then we send the habit to the MCU 
            if "None" not in msg:
                print(msg)
                comms.send_message(msg)

        # if 120 seconds has passed, we check the calender 
        if time.time() - event_time >= 120:
            event_time = time.time()

            msg = calender.checkEvents()

            if "None" not in msg:
                print(msg)
                comms.send_message(msg)

        # if 60 seconds has passed and the timer is on, we check the timer again 
        if timer_on and time.time() - timer_time >= 60:
            timer_time = time.time()
            msg = pomodoro_timer.main_loop()
            if "None" not in msg:
                if 'Good' in msg:
                    timer_on = False
                    comms.send_message(msg)
        # check if any messages sent from the arduino 
        else:
            arduino_msg = comms.receive_message()
            if arduino_msg != None and  "start" in arduino_msg: # if start is sent, we start the timer
                now = datetime.datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                print("Time to Focus! Timer for 30 minutes is starting soon.\n")  
                print("Now: ", dt_string)   
                print("-" * 60)

                timer_on = True


        
if __name__ == "__main__":
    main()