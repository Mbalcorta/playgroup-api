# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import json

def getEventHtml(library):   
    page = urllib.request.urlopen(library)
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
    familyChildEvent = "&tid%5B%5D=16&tid%5B%5D=19"
    avenue81_url = oaklandLibrary+"244"+familyChildEvent
    elmhurst_url = oaklandLibrary+"250"+familyChildEvent
    eastmont_url = oaklandLibrary+"249"+familyChildEvent
    caesar_chavez_url = oaklandLibrary+"247"+familyChildEvent
    melrose_url = oaklandLibrary+"254"+familyChildEvent

    allLibraries = {
        "Avenue81_Library": avenue81_url ,
        "Elmhurst_Library": elmhurst_url,
        "Eastmont_Library": eastmont_url,
        "Caesar_Chavez_Library": caesar_chavez_url,
        "Melrose_Library": melrose_url,
    }   

    locations = {
        "Melrose_Library": {"lat": 37.772424, "lng": -122.20755},
        "Elmhurst_Library": {"lat": 37.7515679, "lng": -122.17491540000003},
        "Avenue81_Library": {"lat": 37.7533954, "lng": -122.18569109999999},
        "Eastmont_Library": {"lat": 37.7681292, "lng": -122.17615089999998},
        "Caesar_Chavez_Library": {"lat": 37.7758485, "lng": -122.22479379999999},
    }

    libraryObject= {}
    # libraryObject["Elmhurst_Library"] = {
    #     'location': locations["Elmhurst_Library"],
    #     'allEvents': getEventHtml(allLibraries["Elmhurst_Library"])
    # }
    
    for eachLibrary in allLibraries.keys():
        libraryObject[eachLibrary] = {
            'location': locations[eachLibrary],
            'allEvents': getEventHtml(allLibraries[eachLibrary])
        }
        

    jsonEvents = json.dumps(libraryObject)
    print(jsonEvents)

libraryObject()