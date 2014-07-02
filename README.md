sun-angle
=========

Given latitude, longitude and gmt date and time - calculate the azimuth and elevation of the Sun's position.

This code derived from a stackexchange question with code originally in the R language.
Here: 
  http://stackoverflow.com/questions/8708048/position-of-the-sun-given-time-of-day-latitude-and-longitude
  
Converted to Python and extensively tested against the NOAA site.
Note NOAA site uses satellite based Lat/Long where East is negative instead of more usual Map based Lat/Long where East is Positive.
Here:
  http://www.esrl.noaa.gov/gmd/grad/solcalc/azel.html
