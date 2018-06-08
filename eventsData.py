# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import json

def getEventHtml(library):   
    page = urllib2.urlopen(library)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div', attrs={'class': 'view-content'})
    eventObjectHtml = []
    eventText = []

    allEventTables = content.find_all("table", class_="views-table cols-3")

    if len(allEventTables) == 0: 
        content = soup.find_all('div', attrs={'class': 'view-content'})[1]
        allEventTables = content.find_all("table", class_="views-table cols-3")

    for index, eachEvent in enumerate(allEventTables):
        eventObjectHtml.append([{ 
            'date': eachEvent.find_all('span')[0],
            'time': eachEvent.find_all('span')[1:], 
            'info': eachEvent.find_all('a')[::2]
            }])

    for index, eventInfo in enumerate(eventObjectHtml):
         date = eventInfo[0]['date'].text.strip()
         eventText.append({ 
             'date': date,
             'eventInfo': []
            })
    
         appendToEventText = eventText[index]['eventInfo']
         eachAnchor = eventObjectHtml[index][0]
         for index, eachElement in enumerate(eachAnchor['info']):
             appendToEventText.append({
                 'eventName': eachElement.text.strip(),
                 'time': eachAnchor['time'][index].text.strip(),
                 'url': 'http://oaklandlibrary.org'+eachElement.attrs['href']
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

    locations = {
        "melrose_library": {"lat": 37.772424, "lng": -122.20755}
    }

    libraryObject= {}
    libraryObject["melrose_library"] = {
        'location': locations["melrose_library"],
        'allEvents': getEventHtml(allLibraries["melrose_library"])
    }
    
    # for eachLibrary in allLibraries.keys():
    #     libraryObject[eachLibrary] = getEventHtml(allLibraries[eachLibrary])

    jsonEvents = json.dumps(libraryObject)
    print(jsonEvents)

libraryObject()