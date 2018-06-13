"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""

import sys

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
          events = service.events().list(calendarId='lotusbloomfamily.org_44ipptdksojiq41drsoce41g68@group.calendar.google.com', pageToken=page_token).execute()
          for event in events['items']:
            if event['summary'] != 'Closed':
                print(event['summary'])
                print(event['description'])
                print(event['start']['dateTime'])
                print(event['']['dateTime'])
          page_token = events.get('nextPageToken')
          if not page_token:
            break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)