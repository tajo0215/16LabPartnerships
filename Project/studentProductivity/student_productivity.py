import os.path
import datetime
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class StudentCalender:

	__scope = ['https://www.googleapis.com/auth/calendar.readonly'] # our calender scope is read only
	__creds = None
	__service = None

	def __init__(self) -> None:
		self.setup()


	def setup(self):
		# The file token.json stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		# Used Quickstart quide for calender api: https://developers.google.com/calendar/quickstart/python

		if os.path.exists('token.json'):
			self.__creds = Credentials.from_authorized_user_file('token.json', self.__scope)
		# If there are no (valid) credentials available, let the user log in.
		if not self.__creds or not self.__creds.valid:
			if self.__creds and self.__creds.expired and self.__creds.refresh_token:
				self.__creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', self.__scope)
				self.__creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.json', 'w') as token:
				token.write(self.__creds.to_json())

		self.__service = build('calendar', 'v3', credentials=self.__creds)


	def getTodayEvents(self):
		now = datetime.datetime.now() 
		end = now + datetime.timedelta(1)

		now = now.isoformat() + "Z" # changes format to DateTTime
		end = end.isoformat() + "Z"

		# gets the events from now until 24 hours later
		events_result = self.__service.events().list(calendarId='primary', timeMin=now, timeMax=end, singleEvents=True, orderBy='startTime').execute()

		# puts it in a list
		events = events_result.get('items', [])

		# returns list of events
		return events

	def checkEvents(self):

		events_today = {} # stores the events that are only today, not in the 24 hr period

		events = self.getTodayEvents() 
		if not events:
			print('No upcoming events found.')
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date')) # gets the start time of the event
			end = event['end'].get('dateTime', event['start'].get('date')) # gets the end time of the event
			start = start[start.find('T') + 1 : start.find('T') + 6] # formats start time for easier manipulation for later
			end = end[end.find('T') + 1 : end.find('T') + 6] # formats end time 
			events_today[start] = event['summary'] + ">" + end # gets the time, and event name

		now = datetime.datetime.now().isoformat()
		idx = now.find('T') # finds the place where date and time are seperated
		now = [int(now[idx + 1:idx + 3]), int(now[idx + 4:idx + 6])] # first entry is hour, second entry is minute

		for start in events_today: # parses through today's events
			start_time = [int(start[:2]), int(start[3:])] # gets the start hour and minute of the event

			if now[0] >= start_time[0] and now[1] >= start_time[1]: # checks if the hour and minute line up 

				end_time = events_today[start][events_today[start].find('>') + 1:] # gets the end time of the event 
				end_time = [int(end_time[:2]), int(end_time[3:])] # formats end time 

				events_today[start] = events_today[start][:events_today[start].find('>')] # sets the event_today entry just to the event name now 

				if int(start_time[0]) > 12: # checks if the event is in 2nd half of day 
					st = str(start_time[0] - 12 ) + ":" + str(start_time[1]) # gets start time
					et = str(end_time[0] - 12) + ":" + str(end_time[1]) # gets end time 

					msg = '' # stores the return message 

					if start_time[1] == 0 and end_time[1] == 0: # checks if its a time less than 10 and minutes equal to 0
						msg = f"event,{st}0 PM,{et}0 PM,{events_today[start]}"
					elif start_time[1] == 0 and end_time[1] != 0:  # checks if its a time less than 10 and minutes not equal to 0
						msg = f"event,{st}0 PM,{et} PM,{events_today[start]}" 
					elif start_time[1] != 0 and end_time[1] == 0:  # checks if a hour greater than 10 and minutes equal to 0 
						msg = f"event,{st} PM,{et}0 PM,{events_today[start]}"
					else: # last possibilityy is hour greater than 10 and minutes not equal to 0
						msg = f"event,{st} PM,{et} PM,{events_today[start]}"
					
					# remove the event from today's events 
					events_today.pop(start)
					return msg # return the message with event name, start time, and end tim 

				else: # for AM events
					st = str(start_time[0]) + ":" + str(start_time[1])
					msg = f"event,{st} AM,{events_today[start]}"
					events_today.pop(start)
					return msg
		return "None"


class Pomodoro:    


	# initialize the variables
	__lastMinute = 0
	__lastMinuteIdx = 0
	__lastMinuteBreak = 0
	__lastMinuteBreakIdx = 0
	__startMinute = 0
	__break = False

	

	def __init__(self):
				
		self.__working_duration = 5
		self.__break_duration = 2
		
	def main_loop(self):              

		now = datetime.datetime.now().isoformat()

		# Get the current minutes of time in integer
		minute = now[now.find('T') + 4: now.find('T') + 6]
		minute = int(minute)

		if self.__startMinute == 0:
			self.__startMinute = minute
		
		# Incrementing __lastMinuteIdx to track the passed minutes from 0
		if minute != self.__lastMinute:
			if minute - self.__lastMinute >= 1:
				self.__lastMinuteIdx += 1 
				self.__lastMinute = minute
		
		# initialize msg
		msg = "None"   

		# If the current index of __lastMinuteIdx equals to 30, prints out Good Job and returning the message
		if self.__lastMinuteIdx - 1 == self.__working_duration and not self.__break:
			msg = "Good Job! Time to Break!"
			self.__break = True
			self.__startMinute = 0
			self.__lastMinuteBreakIdx += 1
			# Increment the lastMinuteBreakIdx to check if it's entering the breaktime
			print(msg + f"({datetime.datetime.now().strftime('%H:%M:%S')})")
			pass
		elif (self.__lastMinuteIdx - 1) % 2 == 0 and self.__lastMinuteIdx - 1 != 0 and not self.__break: # Every two minutes, the program lets us know how many times left
			msg = f"Focus, {self.__working_duration - self.__lastMinuteIdx + 1} mins left"
			print(msg + f"({datetime.datetime.now().strftime('%H:%M:%S')})")
		elif (self.__lastMinuteIdx - 1) == self.__working_duration - 1 and not self.__break: # If 1 minute remaining, it lets us know break time is coming soon
			msg = f"Hang Up, Break Soon!" 
			print(msg + f"({datetime.datetime.now().strftime('%H:%M:%S')})")                   
		   
		# If the current index of __lastMinuteBreakIdx equals to 15, terminates   
		if self.__break:
			if self.__lastMinuteBreakIdx - 1 == self.__break_duration:
				msg = f'Good'
				print("Break Over")
			elif self.__lastMinuteBreakIdx - 1 == self.__break_duration - 1:  # If 1 minute remaining, it lets us know break time is ending soon
				msg = f"Ooops, 1 minute left!"
				print(msg + f"({datetime.datetime.now().strftime('%H:%M:%S')})")
			elif (self.__lastMinuteBreakIdx - 1) % 2 == 0: # Every two minutes, the program lets us know how many times left
				msg = f"Chill, {self.__break_duration - self.__lastMinuteBreakIdx + 1} mins left!"
				print(msg + f"({datetime.datetime.now().strftime('%H:%M:%S')})")  

			if minute != self.__lastMinuteBreak:
				if minute - self.__lastMinuteBreak >= 1:
					self.__lastMinuteBreakIdx += 1
					self.__lastMinuteBreak = minute   
		return msg


class HabitTracker:

	__habits = {} # used to store habits
	__habitFile = "./habits/habit.csv" # file is used to save habits 
	__completedHabits = [] # used to parse habits to check which one we haven't done yet 


	def __init__(self) -> None:

		self.__completedHabits = []

		with open(self.__habitFile, 'r') as habits: # reads the pre-saved habits and saves it to the habits dictionary 
			reader = csv.reader(habits)
			self.__habits = {row[0]:row[1] for row in reader}


	def addHabit(self, habit_name, habit_time) -> None:
		self.__habits[habit_name] = habit_time # the key is the habit name, the value is the time 

		with open(self.__habitFile, "a", newline="") as csvFile: # saves the habit to the CSV file 
			writer = csv.writer(csvFile)
			writer.writerow([habit_name.strip(), habit_time.strip()])
		csvFile.close()

	"""
	This function orders the habits by order in time throughout the day 
	Returns nothing, changes the habit dictionary 
	"""
	def orderHabits(self) -> None:

		temp = {} # used for temporary storage 

		for key, value in self.__habits.items(): # parses through the values of the habits
			if 'AM' in value: # checks if the habit is in the morning 
				temp[key] = value # saves the AM habit to temp 

		# takes out the AM habits from the habits dictionary 
		for key, value in temp.items(): 
			self.__habits.pop(key)

		# adds the AM habits to the begginning of the habit dictionary 
		self.__habits = {**temp, **self.__habits}

		temp = {}

		# orders habits 
		for key, value in self.__habits.items():
			value = value.strip() # strips any whitespace
			time = value[0:5] # gets the time value out of the habit 
			indicator = value[5:].strip() # gets the AM/PM indicator 
			if " " in time: # if the time is less than 10 hours, than we add a zero for ordering purposes
				time = "0" + time
			if "AM" in indicator: # if the time is AM, we add a 1 to the beginning 
				time = "1" + time 
			else: # if the time is PM, we add a 2 to the beginning 
				time = "2" + time

			time = time.replace(":", "") # replace the : with nothing 
			
			temp[key] = int(time.strip()) # make the value into a integer 
		
		self.__habits = {k:v for k,v in sorted(temp.items(), key = lambda item: item[1])} # sort the dictionary by the integers in temp 

		for key, value in self.__habits.items(): # put the temp habits back into habit dictionary 
			value = str(value) # makes value back into string 
			if value[0] == "1": # if the 1 is in the beginning 
				value = value + " AM" # add the AM 
				value = value[1:] # remove the 1 
			else: # same as above but for PM 
				value = value + " PM"
				value = value[1:]
			
			self.__habits[key] = value # add the value to habit dictionary 


	def checkHabits(self) -> str:
		now = datetime.datetime.now().isoformat() # gets current time 
		idx = now.find('T') 
		hour = now[idx +  1 : idx + 3] # gets the hour 
		minute = now[idx + 4: idx + 6] # gets the minute 

		
		for key, value in self.__habits.items(): # parses through dictionary 
			habit_hour = value[0:2] # gets the habit hour 
			habit_min = value[2:5] # gets the habit minute 

			if 'PM' in value[5:]: # checks if its PM, then adds 12 to hour 
				habit_hour = int(habit_hour) + 12
			
			# checks if habit is completed, and if time line up 
			if int(habit_hour) == int(hour) and int(minute) == int(habit_min) and key not in self.__completedHabits: 
				self.__completedHabits.append(key) # adds it to completed habits 

				# returns the habit and time of habit 
				return f'Habit: {key.capitalize()}, Time: {habit_hour}:{habit_min}{value[5:]}'

		return "None"
