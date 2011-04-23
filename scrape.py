from urllib import urlopen
from urlparse import urlparse, parse_qs, urljoin
from BeautifulSoup import BeautifulSoup
import re

# given a URL or HTML, try to extract any structured event data or calendars
# 
# There should also be some sort of ranking, if multiple calendars are available.
#


gcal_link_re=re.compile(r'http[s]*://.+google.com/calendar/.+/((.)+)/public/.+', flags=re.IGNORECASE)



calendars=["http://startupbaltimore.org/events-calendar/",
            'http://www.i3detroit.com/',
            'http://www.birchandbarley.com/calendar.html',
          'http://plancast.com/category/technology/259208#category/7/local',
          'http://www.dctechevents.com/',
          'http://www.hacdc.org/'
          ]

          #  'http://www.hacdc.org/', # links to an iCal file
          #  'http://www.i3detroit.com/', #embeds a google calendar
          #  'http://sites.google.com/site/detroitjug/', #links to an eventbrite page
          #  'http://www.facebook.com/group.php?gid=156512411342&v=app_2344061033', #facebook group with events
          #  'http://www.meetup.com/DC-Tech-Meetup/', #meetup group
          #  http://eventful.com/washingtondc/events?q=Conferences&ga_search=Conferences&ga_type=events&c=technology   links to an ical
          # http://www.dc-flex.com/  embeds  facebook page
      
      
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
            complete_uri=urljoin(uri,dict(link.attrs)['href'])
            discovered.append((complete_uri, 'ical', 10))

    # next, look for embedded google calendars
    found= soup.findAll('iframe', src=re.compile(r'http://www.google.com/calendar.embed?((.)+)', flags=re.IGNORECASE))
    if found: 
        for iframe in found:
            query= urlparse(dict(iframe.attrs)['src']).query
            calendar_id = parse_qs(query)['src']
            discovered.append((calendar_id, 'gdata', 8))

    # now, links to google calendars
    found= soup.findAll('a', href=gcal_link_re)
    if found: 
        gcal_ids=set()  
        for link in found:
            match=gcal_link_re.match(dict(link.attrs)['href'])
            gcal_ids.add(match.group(1).replace('%40','@'))
            #query= urlparse(dict(link.attrs)['href']).query
            #calendar_id = parse_qs(query)['href']
            #discovered.append((calendar_id, 'gdata', 8))
        
        for gcal in gcal_ids:
            discovered.append((gcal, 'gdata', 8))

    

    # webcal:// links
    found=soup.findAll('a',href=re.compile(r'webcal://(.)+',re.IGNORECASE))
    if found: 
        for webcal in found:
            href=dict(webcal.attrs)['href'].replace('webcal://','http://')
            complete_uri=urljoin(uri,href)
            discovered.append((complete_uri, 'ical', 7))
    return discovered
             
    
    
    
if __name__ == '__main__': 
    for calendar_uri in calendars:
      print calendar_uri
      print search_for_calendars(calendar_uri)