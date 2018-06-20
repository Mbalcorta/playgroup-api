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
                print(event['summary'])
                print(event['description'])
                print(event['start']['dateTime'])
                print(event['end']['dateTime'])
          page_token = events.get('nextPageToken')
          if not page_token:
            break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)