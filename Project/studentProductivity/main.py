from ECE16Lib.Communication import Communication
from calender import StudentCalender
import datetime
from ECE16Lib.Communication import Communication
import time

def main():

    calender = StudentCalender()
    comms = Communication("COM5", 115200)

    comms.clear()

    events_today = {}

    event_time = 0

    while True:

        if time.time() - event_time >= 120:
            event_time = time.time()
            events_today.clear()
            events = calender.getTodayEvents()
            if not events:
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['start'].get('date'))

                start = start[start.find('T') + 1 : start.find('T') + 6]
                end = end[end.find('T') + 1 : end.find('T') + 6]

                events_today[start] = event['summary'] + ">" + end

        now = datetime.datetime.now().isoformat()
        idx = now.find('T')
        now = [int(now[idx + 1:idx + 3]), int(now[idx + 4:idx + 6])]

        for start in events_today:
            start_time = [int(start[:2]), int(start[3:])]

            if now[0] >= start_time[0] and now[1] >= start_time[1]: 

                end_time = events_today[start][events_today[start].find('>') + 1:]
                end_time = [int(end_time[:2]), int(end_time[3:])]

                events_today[start] = events_today[start][:events_today[start].find('>')]

                if int(start_time[0]) > 12:
                    st = str(start_time[0] - 12 ) + ":" + str(start_time[1])
                    et = str(end_time[0] - 12) + ":" + str(end_time[1])

                    msg = ''

                    if start_time[1] == 0 and end_time[1] == 0:
                        msg = f"event,{st}0 PM,{et}0 PM,{events_today[start]}"
                    elif start_time[1] == 0 and end_time[1] != 0: 
                        msg = f"event,{st}0 PM,{et} PM,{events_today[start]}"
                    elif start_time[1] != 0 and end_time[1] == 0: 
                        msg = f"event,{st} PM,{et}0 PM,{events_today[start]}"
                    else:
                        msg = f"event,{st} PM,{et} PM,{events_today[start]}"
                    print(msg)
                    comms.send_message(msg)
                else:
                    st = str(start_time[0]) + ":" + str(start_time[1])
                    msg = f"event,{st} AM,{events_today[start]}"
                    comms.send_message(msg)
                events_today.pop(start)
                break
            



if __name__ == "__main__":
    main()
