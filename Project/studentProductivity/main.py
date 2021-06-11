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

    if input("Would you like to add habits today? Y/N") == "Y":
        (name, habit_time) = input("Please input your habit: Habit Name, Habit Time (XX:XX PM/AM Format): ").split(',')
        habitTracker.addHabit(name, habit_time)

        while True:
            if input("Would you like to add another habit? Y/N") == "Y":
                (name, habit_time) = input("Please input your habit: Habit Name, Habit Time (XX:XX PM/AM Format): ").split(',')
                habitTracker.addHabit(name, habit_time)
            else:
                break
    
    habitTracker.orderHabits()
    habit_time = 0
    event_time = 0

    events_today = {}

    timer_on = False

    comms.send_message('Timer Ready')

    while True:

        if time.time() - habit_time >= 10:
            habit_time = time.time()

            msg = habitTracker.checkHabits()

            if "None" not in msg:
                print(msg)
                comms.send_message(msg)


        if time.time() - event_time >= 120:
            event_time = time.time()

            msg = calender.checkEvents()

            if "None" not in msg:
                print(msg)
                comms.send_message(msg)

        if timer_on:
            msg = pomodoro_timer.main_loop()
            if "None" not in msg:
                comms.send_message(msg)

        else:
            arduino_msg = comms.receive_message()
            if arduino_msg != None and  "start" in arduino_msg:
                now = datetime.datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                print("Time to Focus! Timer for 30 minutes is starting soon.\n")  
                print("Now: ", dt_string)   
                print("-" * 60)

                timer_on = True


        
if __name__ == "__main__":
    main()