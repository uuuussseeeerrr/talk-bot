# backend/calendar_utils.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")

# CALENDAR_ID = "60excel@gmail.com"

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'
CALENDAR_ID = os.getenv("CALENDAR_ID")  # set this in .env

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(start_time):
    end_time = datetime.datetime.fromisoformat(start_time) + datetime.timedelta(minutes=30)
    # events = service.events().list(
    #     calendarId=CALENDAR_ID,
    #     timeMin=start_time + 'Z',
    #     timeMax=end_time.isoformat() + 'Z',
    #     singleEvents=True
    # ).execute()
    # 
    events = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=start_time + 'Z',
    timeMax=end_time.isoformat() + 'Z',
    singleEvents=True
    ).execute()
    return len(events['items']) == 0
    


def create_event(name, email, start_time):
    end_time = datetime.datetime.fromisoformat(start_time) + datetime.timedelta(minutes=30)
    event = {
        'summary': f'Meeting with {name}',
        # 'attendees': [{'email': email}],
        'start': {'dateTime': start_time + 'Z', 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat() + 'Z', 'timeZone': 'Asia/Kolkata'},
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    
    
def get_upcoming_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' means UTC
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    upcoming = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No Title')
        upcoming.append({"summary": summary, "start": start})
    return upcoming

