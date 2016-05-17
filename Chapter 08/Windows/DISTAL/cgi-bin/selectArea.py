#!/usr/local/bin/python3

import cgi, os.path, sys
import psycopg2
import mapGenerator

HEADER = "Content-Type: text/html; charset=UTF-8\n\n" \
       + "<html><head><title>Select Area</title>" \
       + "</head><body>"
FOOTER = "</body></html>"
HIDDEN_FIELD = '<input type="hidden" name="{}" value="{}">'


MAX_WIDTH = 600
MAX_HEIGHT = 400

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

form = cgi.FieldStorage()
if "countryID" not in form:
    print(HEADER)
    print('<b>Please select a country</b>')
    print(FOOTER)
    sys.exit(0)

countryID = int(form['countryID'].value)

# Calculate the bounding box.

cursor.execute("SELECT name," +
        "ST_YMin(ST_Envelope(outline))," +
        "ST_XMin(ST_Envelope(outline))," +
        "ST_YMax(ST_Envelope(outline))," +
        "ST_XMax(ST_Envelope(outline)) " +
        "FROM countries WHERE id=%s", (countryID,))

row = cursor.fetchone()
if row != None:
    name    = row[0]
    minLat  = row[1]
    minLong = row[2]
    maxLat  = row[3]
    maxLong = row[4]
else:
    print(HEADER)
    print('<b>Missing country</b>')
    print(FOOTER)
    sys.exit(0)

minLong = minLong - 0.2
minLat = minLat - 0.2
maxLong = maxLong + 0.2
maxLat = maxLat + 0.2

# Calculate the map's dimensions.

width = float(maxLong - minLong)
height = float(maxLat - minLat)
aspectRatio = width/height

mapWidth = MAX_WIDTH
mapHeight = int(mapWidth / aspectRatio)

if mapHeight > MAX_HEIGHT:
    # Scale the map to fit.
    scaleFactor = float(MAX_HEIGHT) / float(mapHeight)
    mapWidth = int(mapWidth * scaleFactor)
    mapHeight = int(mapHeight * scaleFactor)

# Generate the map.

hilite = "[id] = " + str(countryID)
imgFile = mapGenerator.generateMap("countries",
                                   minLong, minLat,
                                   maxLong, maxLat,
                                   mapWidth, mapHeight,
                                   hiliteExpr=hilite)

# Display the results.

print(HEADER)
print('<b>' + name + '</b>')
print('<p>')
print('<form method="POST" action="showResults.py">')
print('Select all features within')
print('<input type="text" name="radius" value="10" size="2">')
print('miles of a point.')
print('<p>')
print('Click on the map to identify your starting point:')
print('<br>')
print('<input type="image" src="' + imgFile + '" ismap>')
print(HIDDEN_FIELD.format("countryID", countryID))
print(HIDDEN_FIELD.format("countryName", name))
print(HIDDEN_FIELD.format("mapWidth", mapWidth))
print(HIDDEN_FIELD.format("mapHeight", mapHeight))
print(HIDDEN_FIELD.format("minLong", minLong))
print(HIDDEN_FIELD.format("minLat", minLat))
print(HIDDEN_FIELD.format("maxLong", maxLong))
print(HIDDEN_FIELD.format("maxLat", maxLat))
print('</form>')
print(FOOTER)

