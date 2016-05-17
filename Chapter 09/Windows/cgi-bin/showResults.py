#!/usr/local/bin/python3

#!/usr/bin/env python

import psycopg2
import cgi
import pyproj

import mapGenerator

############################################################

HEADER = "Content-Type: text/html; charset=UTF-8\n\n" \
       + "<html><head><title>Search Results</title>" \
       + "</head><body>"
FOOTER = "</body></html>"


MAX_WIDTH = 800
MAX_HEIGHT = 600

METERS_PER_MILE = 1609.344

############################################################

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

# Extract our CGI parameters.

form = cgi.FieldStorage()

countryID   = int(form['countryID'].value)
radius      = int(form['radius'].value)
x           = int(form['x'].value)
y           = int(form['y'].value)
mapWidth    = int(form['mapWidth'].value)
mapHeight   = int(form['mapHeight'].value)
countryName = form['countryName'].value
minLong     = float(form['minLong'].value)
minLat      = float(form['minLat'].value)
maxLong     = float(form['maxLong'].value)
maxLat      = float(form['maxLat'].value)

# Calculate the clicked-on point.

xFract = float(x)/float(mapWidth)
longitude = minLong + xFract * (maxLong-minLong)

yFract = float(y)/float(mapHeight)
latitude = minLat + (1-yFract) * (maxLat-minLat)

# Identify matching placenames.

cursor.execute("SELECT ST_X(position::geometry), " +
               "ST_Y(position::geometry),name " +
               "FROM places WHERE " +
               "ST_DWithin(position, ST_MakePoint(%s, %s), %s)",
               (longitude, latitude, radius * METERS_PER_MILE))

points = []
for long,lat,name in cursor:
    points.append([long, lat, name])

# Calculate the map's bounding box.

geod = pyproj.Geod(ellps="WGS84")
distance = radius * METERS_PER_MILE * 1.1 # Add 10% buffer.

x,y,angle = geod.fwd(longitude, latitude, 0, distance)
maxLat = y

x,y,angle = geod.fwd(longitude, latitude, 90, distance)
maxLong = x

x,y,angle = geod.fwd(longitude, latitude, 180, distance)
minLat = y

x,y,angle = geod.fwd(longitude, latitude, 270, distance)
minLong = x

# Generate the map.

iLat = int(round(latitude))
iLong = int(round(longitude))

subSelect = "(SELECT outline FROM tiled_shorelines" \
          + " WHERE (intLat={})".format(iLat) \
          + " AND (intLong={})".format(iLong) \
          + ") AS shorelines"

imgFile = mapGenerator.generateMap(subSelect,
                                   minLong, minLat,
                                   maxLong, maxLat,
                                   MAX_WIDTH, MAX_HEIGHT,
                                   points=points)

# Display the results.

print(HEADER)
print('<b>' + countryName + '</b>')
print('<p>')
print('<img src="' + imgFile + '">')
print(FOOTER)

