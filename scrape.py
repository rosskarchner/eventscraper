from urllib import urlopen
from urlparse import urlparse, parse_qs
from BeautifulSoup import BeautifulSoup
import re

#given a URL or HTML, try to extract any structured event data or syndicat-able calendars


calendars=['http://www.i3detroit.com/',
            'http://www.birchandbarley.com/calendar.html',
          'http://plancast.com/category/technology/259208#category/7/local',
          'http://www.dctechevents.com/']
          #'http://startupbaltimore.org/events-calendar/',   #links to a google calendar
          #  'http://www.hacdc.org/', # links to an iCal file
          #  'http://www.i3detroit.com/', #embeds a google calendar
          #  'http://sites.google.com/site/detroitjug/', #links to an eventbrite page
          #  'http://www.facebook.com/group.php?gid=156512411342&v=app_2344061033', #facebook group with events
          #  'http://www.meetup.com/DC-Tech-Meetup/', #meetup group
          #  ]
      
      
def search_for_calendars(uri):
    html= urlopen(uri).read()
    soup = BeautifulSoup(html)
    # search for <link rel=alternate type=text/calendar />  
    # This should always win.
    discovered=[]
    found = soup.findAll('link', rel=re.compile(r'ALTERNATE', flags=re.IGNORECASE),
                      type=re.compile(r'text/calendar', flags=re.IGNORECASE ))
    if found: 
        for link in found:
            discovered.append((dict(link.attrs)['href'], 'ical', 10))
    # next, look for embedded google calendars
    found= soup.findAll('iframe', src=re.compile(r'http://www.google.com/calendar.embed?((.)+)', flags=re.IGNORECASE))
    if found: 
        for iframe in found:
            query= urlparse(dict(iframe.attrs)['src']).query
            calendar_id = parse_qs(query)['src']
            discovered.append((calendar_id, 'gdata', 8))
    found=soup.findAll('a',href=re.compile(r'webcal://(.)+',re.IGNORECASE))
    if found: 
        print found
    return discovered
             
    
    
    
    
    
for calendar_uri in calendars:
    print search_for_calendars(calendar_uri)