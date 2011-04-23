This module attempts to scrape a page for any and all links and embeds that might offer a hint about related (structured) calendar data.

Right now, it's a messy pile of hacks, but I'll eventually adding tests and making it a proper python package.

What works now: 
* detecting "link" tags with rel="alternate", type="text/calendar"   (returns the iCal URI)
* detecting embedded and linked to Google Calendars (returns the gcal ID)
* links using the webcal:// scheme (returns the links, converted to 'http://')