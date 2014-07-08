sun-angle
=========

Given latitude, longitude and gmt date and time - calculate the azimuth and elevation of the Sun's position.

This code derived from a stackexchange question with code originally in the R language.

Here: http://stackoverflow.com/questions/8708048/position-of-the-sun-given-time-of-day-latitude-and-longitude
  
Converted to Python and extensively tested against the NOAA site.

Note NOAA site uses satellite based Lat/Long where East is negative instead of more usual Map based Lat/Long where East is Positive.

Here: http://www.esrl.noaa.gov/gmd/grad/solcalc/azel.html

Usage:
```
lat = 
sun_position(2014,7,1, lat=-11.953349, longitude=-76.992187) # returns azimuth and elevation for noon(GMT) on July1 2014

latlong_str_conversion("38°43'26.724N 9°8'26.25W") # converts to lat, long as floats for input to sun_position

latlong_float_conversion(-11.953349, -76.992187) # returns the string versio of lat long in NSEW notation shown above.
```