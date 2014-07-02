#!/usr/python

# from R
"""
sunPosition <- function(year, month, day, hour=12, min=0, sec=0,
                    lat=46.5, long=6.5) {

    twopi <- 2 * pi
    deg2rad <- pi / 180

    # Get day of the year, e.g. Feb 1 = 32, Mar 1 = 61 on leap years
    month.days <- c(0,31,28,31,30,31,30,31,31,30,31,30)
    day <- day + cumsum(month.days)[month]
    leapdays <- year %% 4 == 0 & (year %% 400 == 0 | year %% 100 != 0) & 
                day >= 60 & !(month==2 & day==60)
    day[leapdays] <- day[leapdays] + 1

    # Get Julian date - 2400000
    hour <- hour + min / 60 + sec / 3600 # hour plus fraction
    delta <- year - 1949
    leap <- trunc(delta / 4) # former leapyears
    jd <- 32916.5 + delta * 365 + leap + day + hour / 24

    # The input to the Atronomer's almanach is the difference between
    # the Julian date and JD 2451545.0 (noon, 1 January 2000)
    time <- jd - 51545.

    # Ecliptic coordinates

    # Mean longitude
    mnlong <- 280.460 + .9856474 * time
    mnlong <- mnlong %% 360
    #mnlong[mnlong < 0] <- mnlong[mnlong < 0] + 360

    # Mean anomaly
    mnanom <- 357.528 + .9856003 * time
    mnanom <- mnanom %% 360
    mnanom[mnanom < 0] <- mnanom[mnanom < 0] + 360
    mnanom <- mnanom * deg2rad

    # Ecliptic longitude and obliquity of ecliptic
    eclong <- mnlong + 1.915 * sin(mnanom) + 0.020 * sin(2 * mnanom)
    eclong <- eclong %% 360
    eclong[eclong < 0] <- eclong[eclong < 0] + 360
    oblqec <- 23.439 - 0.0000004 * time
    eclong <- eclong * deg2rad
    oblqec <- oblqec * deg2rad

    # Celestial coordinates
    # Right ascension and declination
    num <- cos(oblqec) * sin(eclong)
    den <- cos(eclong)
    ra <- atan(num / den)
    ra[den < 0] <- ra[den < 0] + pi
    ra[den >= 0 & num < 0] <- ra[den >= 0 & num < 0] + twopi
    dec <- asin(sin(oblqec) * sin(eclong))

    # Local coordinates
    # Greenwich mean sidereal time
    gmst <- 6.697375 + .0657098242 * time + hour
    gmst <- gmst %% 24
    gmst[gmst < 0] <- gmst[gmst < 0] + 24.

    # Local mean sidereal time
    lmst <- gmst + long / 15.
    lmst <- lmst %% 24.
    lmst[lmst < 0] <- lmst[lmst < 0] + 24.
    lmst <- lmst * 15. * deg2rad

    # Hour angle
    ha <- lmst - ra
    ha[ha < -pi] <- ha[ha < -pi] + twopi
    ha[ha > pi] <- ha[ha > pi] - twopi

    # Latitude to radians
    lat <- lat * deg2rad

    # Solar zenith angle
    zenithAngle <- acos(sin(lat) * sin(dec) + cos(lat) * cos(dec) * cos(ha))
    # Solar azimuth
    az <- acos(((sin(lat) * cos(zenithAngle)) - sin(dec)) / (cos(lat) * sin(zenithAngle)))
    rm(zenithAngle)

    # Azimuth and elevation
    el <- asin(sin(dec) * sin(lat) + cos(dec) * cos(lat) * cos(ha))

    el <- el / deg2rad
    az <- az / deg2rad
    lat <- lat / deg2rad

    # -----------------------------------------------
    # Azimuth correction for Hour Angle
    if (ha > 0) az <- az + 180 else az <- 540 - az
    az <- az %% 360

    return(list(elevation=el, azimuth=az))
}
"""
import math

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

    
def sun_position(year, month, day, hour=12, minute=0, sec=0,
                lat=46.5, longitude=6.5):

    twopi = 2 * math.pi
    deg2rad = math.pi / 180

    time = calc_time(year, month, day, hour, minute, sec)

    # Ecliptic coordinates
    # Mean longitude
    mnlong = 280.46 + 0.9856474 * time
    mnlong = mnlong % 360
    if mnlong < 0: mnlong += 360

    # Mean anomaly
    mnanom = 357.528 + 0.9856003 * time
    mnanom = mnanom % 360
    if mnanom < 0: mnanom += 360
    mnanom = mnanom * deg2rad

    # Ecliptic longitude and obliquity of ecliptic
    eclong = mnlong + 1.915 * math.sin(mnanom) + 0.02 * math.sin(2 * mnanom)
    eclong = eclong % 360
    if eclong < 0: eclong += 360
    oblqec = 23.439 - 0.0000004 * time
    eclong = eclong * deg2rad
    oblqec = oblqec * deg2rad

    # Celestial coordinates
    # Right ascension and declination
    num = math.cos(oblqec) * math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan(num / den)
    if den < 0: ra += math.pi
    if den >= 0 and num < 0: ra += twopi
    dec = math.asin(math.sin(oblqec) * math.sin(eclong))

    # Local coordinates
    # Greenwich mean sidereal time
    gmst = 6.697375 + 0.0657098242 * time + hour
    gmst = gmst % 24
    if gmst < 0: gmst += 24

    # Local mean sidereal time
    lmst = gmst + longitude / 15.0
    lmst = lmst % 24
    if lmst < 0: lmst += 24
    lmst = lmst * 15 * deg2rad

    # Hour angle
    ha = lmst - ra
    if ha < -math.pi: ha += twopi
    if ha > math.pi: ha -= twopi

    # Latitude to radians
    lat = lat * deg2rad

##    # Azimuth and elevation
##    el = math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha))
##    az = math.asin(-math.cos(dec) * math.sin(ha) / math.cos(el))
##
##    # For logic and names, see Spencer, J.W. 1989. Solar Energy. 42(4):353
##    cosAzPos = 0 <= math.sin(dec) - math.sin(el) * math.sin(lat)
##    sinAzNeg = math.sin(az) < 0
##    #print " ", cosAzPos, sinAzNeg
##    if cosAzPos and sinAzNeg: az += twopi
##    if not(cosAzPos): az = math.pi - az
    # Solar zenith angle
    zenithAngle = math.acos(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(ha))
    # Solar azimuth
    az = math.acos(((math.sin(lat) * math.cos(zenithAngle)) - math.sin(dec)) / (math.cos(lat) * math.sin(zenithAngle)))
    #rm(zenithAngle)
    el = math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha))
    
    el = el / deg2rad
    az = az / deg2rad
    lat = lat / deg2rad

    # Azimuth correction for Hour Angle
    if ha > 0:
        #print "  corrected az. +180", az
        #print "    fix?", (az+180-(az*2)) %360
        az += 180
    else:
        #print "  corrected az. 540-az", az
        #print "    fix?", (540+az) %360
        az = 540 - az
    az = az % 360
    return(az, el)

#  A latitude or longitude with 8 decimal places pinpoints a location to within 1 millimeter,( 1/16 inch).
#   Precede South latitudes and West longitudes with a minus sign.
#    Latitudes range from -90 to 90.
#    Longitudes range from -180 to 180.
#    E.g.
#    41.25 and -120.9762
#    -31.96 and 115.84
#    90 and 0 (North Pole)



if __name__ == '__main__':
    ### Tests
    # Latitude: North = +, South = -
    # Longitude: East = -, West = +
    # For July 1 2014
    samples = [(46.5,6.5, 163.03, 65.83),
               (46.0,6.0, 163.82, 66.41),
               (-41,0,    0.98, 25.93),
               (-3,0,     2.01,63.9),
               (3,0,      2.58, 69.89),
               (41,0,     177.11, 72.07),
               (40,0,     176.95, 73.07),
               (-40,0,    0.99, 26.93),
               (-40,40,   38.91, 16.31),
               (-40,-40,  322.67, 17.22),
               (-20,-100, 289.35, -15.64),
               (20,-100,  29.47, 0.4),
               (80,-100,  283.05, 21.2),
               (80,-20,   200.83, 32.51),
               (80,0,     178.94, 33.11),
               (80,40,    135.6, 30.47),
               (80,120,   55.89, 17.74),
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
