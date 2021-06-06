import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class StudentCalender:

    __scope = ['https://www.googleapis.com/auth/calendar.readonly']
    __creds = None
    __service = None

    def __init__(self) -> None:
        self.setup()


    def setup(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
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
        now = datetime.datetime.now() # 'Z' indicates UTC time
        end = now + datetime.timedelta(1)

        now = now.isoformat() + "Z"
        end = end.isoformat() + "Z"

        print(now)

        events_result = self.__service.events().list(calendarId='primary', timeMin=now, timeMax=end, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

