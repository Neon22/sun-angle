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
lat = -11.953349
lon = -76.992187
# returns azimuth and elevation for noon(GMT) on July1 2014
sun_position(2014,7,1, lat=lat, longitude=lon)
# can also define time.
sun_position(year, month, day, hour=12, minute=0, sec=0, lat=46.5, longitude=6.5)

# converts input string in NSEW notation into lat, long as floats
# - for input to sun_position
latlong_str_conversion("38°43'26.724N 9°8'26.25W")
# also accepts extra spaces, missing seconds, decimal minutes.
# E.g.
#  "11° 57.200964S  76° 59.53125W"
#  "38.72409°N 9.140625°W"

# returns the string version of lat long in NSEW notation shown above.
latlong_float_conversion(-11.953349, -76.992187)
```