# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

def getEventHtml(library):   
    page = urllib2.urlopen(library)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div', attrs={'class': 'view-content'})
    eventObject = []
    eventText = []

    allEventTables = content.find_all("table", class_="views-table cols-3")

    for eachEvent in allEventTables:
        eventObject.append( { 
            'date': eachEvent.find_all('span')[0],
            'time': eachEvent.find_all('span')[1:], 
            'info': eachEvent.find_all('a')[::2]
            })

    for eventInfo in eventObject: 
         date = eventInfo['date'].text.strip()

         for index, eachTime in enumerate(eventInfo['time']):
            info =  eventInfo['info'][index].text.strip()
            time =  eachTime.text.strip()

         eventText.append({ 
             'date': date,
             'info': info,
             'time': time
         })

    return  eventText
    

def libraryObject():
    oaklandLibrary = "http://oaklandlibrary.org/events?field_eventlocation_nid%5B%5D="
    familyChildEvent = "&tid%5B%5D=16"
    avenue81_url = oaklandLibrary+"244"+familyChildEvent
    elmhurst_url = oaklandLibrary+"250"+familyChildEvent
    eastmont_url = oaklandLibrary+"249"+familyChildEvent
    caesar_chavez_url = oaklandLibrary+"247"+familyChildEvent
    melrose_url = oaklandLibrary+"254"+familyChildEvent

    allLibraries = {
        "avenue81_library": avenue81_url ,
        "elmhurst_library": elmhurst_url,
        "eastmont_library": eastmont_url,
        "caesar_chavez_library": caesar_chavez_url,
        "melrose_library": melrose_url,
    }   

    libraryObject = []

    for eachLibrary in allLibraries.keys():
        libraryObject.append({
            eachLibrary: getEventHtml(allLibraries[eachLibrary])
        })

    print(libraryObject)

libraryObject()