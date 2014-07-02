#!/usr/python
# -*- coding: cp1252 -*-

# Taken from the code on stackexchange here:
# - http://stackoverflow.com/questions/8708048/position-of-the-sun-given-time-of-day-latitude-and-longitude
# converted into Python and extensively tested.

# It is critical to note the following:
# Latitude is defined as +-90 degrees where 0 is the equator and +90 is the North Pole.
# Longitude is +- 180 degrees about the GMT line, but has two representations:
#  - Either a map based mode where +ve values lie to the East,
#  - or a satellite based mode where +ve refers to the West.
# The NOAA site - where you can validate this code output - uses the satellite basis.
#   - http://www.esrl.noaa.gov/gmd/grad/solcalc/azel.html
# Most maps, and this code, use the Map basis.

#  A latitude or longitude with 8 decimal places pinpoints a location to within 1 millimeter,( 1/16 inch).
#   Precede South latitudes and West longitudes with a minus sign.

# This can be overcome by entering Lat/Long in the NSEW notation instead of as floating point numbers.
# Samples site:
#    - http://www.findlatitudeandlongitude.com/
# E.g. These are equivalent - for Lisbon in Portugal.
#   Latitude:N 38° 43' 26.7257"
#   Longitude:W 9° 8' 26.25"
#   Latitude:N 38° 43.445428'
#   Longitude:W 9° 8.4375'
#   Latitude:38.72409°
#   Longitude:-9.140625°
#
# for Lima Peru
#   Latitude:S 11° 57' 12.0578"
#   Longitude:W 76° 59' 31.875"
#   Latitude:S 11° 57.200964'
#   Longitude:W 76° 59.53125'
#   Latitude:-11.953349°
#   Longitude:-76.992187°


import math, re
# Note: re moduule only used for parsing lat long from string

def present_seconds(seconds):
    """ strip off useless zeros or return nothing if zero
        - this algorithm only good to about 1 decimal place in seconds...
    """
    if seconds == 0:
        # not needed at all
        seconds = ''
    elif seconds - int(seconds) == 0:
        #no need for trailing zeros
        seconds = "%d" % int(seconds)
    else:
        # present with decimals
        seconds = "%2.2f" % seconds
        seconds = seconds.strip('0') # remove unused zeros
    return seconds

def latlong_float_conversion(latitude, longitude):
    """ Convert from floating values into DMS Sexagesimal notation
    """
    # determine direction from sign
    lat = 'N' if latitude >= 0 else 'S'
    lon = 'E' if longitude >= 0 else 'W'
    #
    latitude = abs(latitude)
    longitude = abs(longitude)
    lat_d = int(latitude)
    lat_mf = 60 * (latitude - lat_d)
    lat_m = int(lat_mf)
    lat_s = 60 * (lat_mf - lat_m)
    #
    lon_d = int(longitude)
    lon_mf = 60 * (longitude - lon_d)
    lon_m = int(lon_mf)
    lon_s = 60 * (lon_mf - lon_m)
    # simplify seconds visually
    lat_s = present_seconds(lat_s)
    lon_s = present_seconds(lon_s)
    #
    res = "%d°%d'%s%s %d°%d'%s%s" % (lat_d, lat_m, lat_s, lat, lon_d, lon_m, lon_s, lon)
    return res

def parse_digits(value):
    expr = "^([\d]+[\d\.]*)[^\d][\s]*([\d]+[\d\.]*)[^\d]*([\d\.]*)"
    groups = []
    #print "",value
    m = re.match(expr, value, re.I|re.M)
    try:
        groups = m.groups()
    except:
        pass
    print groups
    res = [a if a else 0 for a in groups]
    for i in range(len(res)):
        val = float(res[i])
        if val - int(val) == 0:
            # its an int
            res[i] = int(res[i])
        else:
            res[i] = val
    #print res
    return res
    
def latlong_str_conversion(latlong):
    " parse a DMS string return floats for lat, lon "
    latlong = latlong.upper()
    lat = lon = False
    n = latlong.find('N')
    s = latlong.find('S')
    e = latlong.find('E')
    w = latlong.find('W')
    #print n,s,e,w, latlong
    if n > 0 or s > 0:
        lat = latlong[:n+s+1].strip()
        if e >0 or w > 0 and n+s+2 <= len(latlong):
            lon = latlong[n+s+2:e+w+1].strip()
    #print "#",lat
    #print "#",lon
    lat_tuple = parse_digits(lat)
    #lat_tuple = [int(a) if a else 0 for a in lat_tuple]
    lon_tuple = parse_digits(lon)
    #lon_tuple = [int(a) if a else 0 for a in lon_tuple]
    #print lat_tuple, lon_tuple
    latitude = lat_tuple[0]+lat_tuple[1]/60.0 + lat_tuple[2]/3600.0
    if s > 0: latitude = -latitude
    longitude = lon_tuple[0]+lon_tuple[1]/60.0 + lon_tuple[2]/3600.0
    if w > 0: longitude = -longitude
    return (latitude, longitude)
    
    

def leapyear(year):  
    if year % 400 == 0:   return True
    elif year % 100 == 0: return False  
    elif year % 4 == 0:   return True  
    else: return False
    

def calc_time(year, month, day, hour=12, minute=0, sec=0):
    # Get day of the year, e.g. Feb 1 = 32, Mar 1 = 61 on leap years
    month_days = [0,31,28,31,30,31,30,31,31,30,31,30]
    day = day + sum(month_days[:month])
    leapdays = leapyear(year) and day >= 60 and (not (month==2 and day==60))
    if leapdays: day += 1

    # Get Julian date - 2400000
    hour = hour + minute / 60.0 + sec / 3600.0 # hour plus fraction
    delta = year - 1949
    leap = delta // 4 # former leapyears
    jd = 32916.5 + delta * 365 + leap + day + hour / 24.0
    # The input to the Astronomer's almanac is the difference between
    # the Julian date and JD 2451545.0 (noon, 1 January 2000)
    time = jd - 51545
    return time


def meanLongitudeDegrees(time):
    return ((280.460 + 0.9856474 * time) % 360)

def meanAnomalyRadians(time):
    return (math.radians((357.528 + 0.9856003 * time) % 360))

def eclipticLongitudeRadians(mnlong, mnanomaly):
    return (math.radians((mnlong + 1.915 * math.sin(mnanomaly) + 0.020 * math.sin(2 * mnanomaly)) % 360))


def eclipticObliquityRadians(time):
    return (math.radians(23.439 - 0.0000004 * time))

def rightAscensionRadians(oblqec, eclong):
    num = math.cos(oblqec) * math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan(num / den)
    if den<0: ra += math.pi
    if (den >= 0 and num < 0): ra += 2 * math.pi
    return (ra)

def rightDeclinationRadians(oblqec, eclong):
    return (math.asin(math.sin(oblqec) * math.sin(eclong)))

def greenwichMeanSiderealTimeHours(time, hour):
    return ((6.697375 + 0.0657098242 * time + hour) % 24)

def localMeanSiderealTimeRadians(gmst, longitude):
    return (math.radians(15 * ((gmst + longitude / 15.0) % 24)))

def hourAngleRadians(lmst, ra):
    return (((lmst - ra + math.pi) % (2 * math.pi)) - math.pi)

def elevationRadians(lat, dec, ha):
    return (math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha)))

##def solarAzimuthRadiansJosh(lat, dec, ha, el):
##    az = math.asin(-math.cos(dec) * math.sin(ha) / math.cos(el))
##    cosAzPos = 0 <= math.sin(dec) - math.sin(el) * math.sin(lat)
##    sinAzNeg = math.sin(az) < 0
##    if (cosAzPos and sinAzNeg): az += 2 * math.pi
##    if not cosAzPos: az = math.pi-az
##    return (az)

def solarAzimuthRadiansCharlie(lat, dec, ha):
    zenithAngle = math.acos(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(ha))
    az = math.acos((math.sin(lat) * math.cos(zenithAngle) - math.sin(dec)) / (math.cos(lat) * math.sin(zenithAngle)))
    if ha > 0:
        az = az + math.pi
    else:
        az = (3 * math.pi - az) % (2 * math.pi)
    return (az)

def sun_position(year, month, day, hour=12, minute=0, sec=0,
                lat = 46.5, longitude = 6.5):

    time = calc_time(year, month, day, hour, minute, sec)
    hour = hour + minute / 60.0 + sec / 3600.0
    # Ecliptic coordinates  
    mnlong = meanLongitudeDegrees(time)   
    mnanom = meanAnomalyRadians(time)  
    eclong = eclipticLongitudeRadians(mnlong, mnanom)     
    oblqec =  eclipticObliquityRadians(time)
    # Celestial coordinates
    ra = rightAscensionRadians(oblqec, eclong)
    dec = rightDeclinationRadians(oblqec, eclong)
    # Local coordinates
    gmst = greenwichMeanSiderealTimeHours(time, hour)  
    lmst =localMeanSiderealTimeRadians(gmst, longitude)
    # Hour angle
    ha = hourAngleRadians(lmst, ra)
    # Latitude to radians
    lat = math.radians(lat)
    # Azimuth and elevation
    el = elevationRadians(lat, dec, ha)
    #azJ = solarAzimuthRadiansJosh(lat, dec, ha, el)
    azC = solarAzimuthRadiansCharlie(lat, dec, ha)

    elevation = math.degrees(el)
##    azimuthJ  = math.degrees(azJ)
    azimuth  = math.degrees(azC)
    return ( azimuth, elevation)


###
if __name__ == '__main__':
    ### Tests
    # Latitude: North = +, South = -
    # Longitude: East = +, West = -
    # For July 1 2014
    samples = [(46.5,-6.5, 163.03, 65.83),
               (46.0,-6.0, 163.82, 66.41),
               (-41,0,    0.98, 25.93),
               (-3,0,     2.01,63.9),
               (3,0,      2.58, 69.89),
               (41,0,     177.11, 72.07),
               (40,0,     176.95, 73.07),
               (-40,0,    0.99, 26.93),
               (-40,-40,   38.91, 16.31),
               (-40,40,  322.67, 17.22),
               (-20,100, 289.35, -15.64),
               (20,-100,  64.62, -1.55),
               (80,100,  283.05, 21.2),
               (80,20,   200.83, 32.51),
               (80,0,     178.94, 33.11),
               (80,-40,    135.6, 30.47),
               (80,-120,   55.89, 17.74),
               (0, 0,     2.26, 66.89)
               ]
    print "Noon July 1 2014 at 0,0 = 2.26, 66.89"
    print "",sun_position(2014,7,1, lat=0, longitude=0)
    print "Noon Dec 22 2012 at 41,0 = 180.03, 25.6"
    print "",sun_position(2012, 12, 22, lat=41, longitude=0)
    print "Noon Dec 22 2012 at -41,0 = 359.09, 72.44"
    print "",sun_position(2012, 12, 22, lat=-41, longitude=0)
    print

    for s in samples:
        lat, lon, az, el = s
        print "\nFor lat,long:", lat, lon,
        calc_az, calc_el = sun_position(2014,7,1, lat=lat, longitude=lon)
        az_ok = abs(az-calc_az) < 0.5
        el_ok = abs(el-calc_el) < 0.5
        if not(az_ok and el_ok):
            print "\n Azimuth (Noaa,calc)   = %4.2f %4.2f (error %4.2f)" %(az, calc_az, abs(az-calc_az))
            print " Elevation (Noaa,calc) = %4.2f %4.2f (error %4.2f)" %(el, calc_el, abs(el-calc_el))
        else:
            print" OK (<0.5 error)"

    #
    print "\nTesting float to string"
    latlong = [(38.72409, -9.140625), (-11.953349, -76.992187), (12, 12), (-22.5, 22.5), (-33.125,-33.125), (44, -44)]
    for (lat, lon) in latlong:
        print lat, lon, "=", latlong_float_conversion(lat, lon)
    #
    print "\nTesting string parsing"
    latlong = ["38°43'26.724N 9°8'26.25W",
               "33°7'30S 33°7'30W",
               "38° 43' 26.724 N 9° 8' 26.25 W",
               "33° 7' 30 S 33°7W",
               "11° 57' 12.0578S  76° 59' 31.875 W",
               "11° 57.200964S  76° 59.53125W",
               "38.72409°N 9.140625°W"
               ]
    for s in latlong:
        print s
        print "", latlong_str_conversion(s)
    
