"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""

import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

from oauth2client import client
from googleapiclient import sample_tools



def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')
    allEvents = []
    try:
        page_token = None
        while True:
          today = datetime.today()
          monthAgo = today - relativedelta(months=1)
          tmax = today.isoformat('T') + "Z"
          tmin = monthAgo.isoformat('T') + "Z"
          events = service.events().list(calendarId='lotusbloomfamily.org_44ipptdksojiq41drsoce41g68@group.calendar.google.com', 
          timeMin=tmin,
          timeMax=tmax,
          singleEvents=True,
          orderBy='startTime',
          pageToken=page_token).execute()
          for event in events['items']:
            if event['summary'] != 'Closed':
                eventName = event['summary'] +', '+ event['description']
                allEvents.append({
                    'date': event['start']['dateTime'],
                    'eventInfo': [{
                        'eventName': eventName,
                        'url': 'http://www.lotusbloomfamily.org/allendale.html',
                        'time': event['end']['dateTime']
                    }] 
                })
                print(datetime(*(time.strptime(event['start']['dateTime'], format)[0:6])))
                # print(allEvents)
          page_token = events.get('nextPageToken')
          if not page_token:
            break
    
# need to return data as so and saved to database
# {'Allendale_School': {'allEvents': [{'date': 'Thursday, June 21st, 2018', 'eventInfo':[{"eventName": "Oakland Symphony Instrument Petting Zoo", "url": "http://oaklandlibrary.org/events/melrose-branch/oakland-symphony-instrument-petting-zoo-0", "time":"1:00pm"}]}], "location": {"lat": 37.7515679, "lng": -122.17491540000003}}}
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)