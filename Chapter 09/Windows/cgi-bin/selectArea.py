#!/usr/local/bin/python3

import cgi, os.path, sys
import psycopg2
import mapGenerator

HEADER = "\n".join([
    "Content-Type: text/html; charset=UTF-8",
    "",
    "",
    "<html><head><title>Select Area</title>",
    "<script type='text/javascript'>",
    "  function onClick(e) {",
    "    e = e || window.event;",
    "    if (e.shiftKey) {",
    "      var target = e.target || e.srcElement;",
    "      var rect = target.getBoundingClientRect();",
    "      var offsetX = e.clientX - rect.left;",
    "      var offsetY = e.clientY - rect.top;",
    "      var countryID = document.getElementsByName('countryID')[0].value;",
    "      var minLat = document.getElementsByName('minLat')[0].value;",
    "      var minLong = document.getElementsByName('minLong')[0].value;",
    "      var maxLat = document.getElementsByName('maxLat')[0].value;",
    "      var maxLong = document.getElementsByName('maxLong')[0].value;",
    "      var zoom = document.getElementsByName('zoom')[0].value;",
    "      var new_zoom = parseInt(zoom, 10) + 1;",
    "      window.location.href = 'selectArea.py'",
    "                           + '?countryID=' + countryID",
    "                           + '&minLat=' + minLat",
    "                           + '&minLong=' + minLong",
    "                           + '&maxLat=' + maxLat",
    "                           + '&maxLong=' + maxLong",
    "                           + '&zoom=' + new_zoom",
    "                           + '&x=' + offsetX",
    "                           + '&y=' + offsetY;",
    "      return false;",
    "    } else {",
    "      return true;",
    "    }",
    "  }",
    "</script>",
    "</head><body>"])
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

if "x" in form:
    click_x = int(form['x'].value)
else:
    click_x = None

if "y" in form:
    click_y = int(form['y'].value)
else:
    click_y = None

if "zoom" in form:
    zoom = int(form['zoom'].value)
else:
    zoom = 0

if ("minLat" in form and "minLong" in form and
    "maxLat" in form and "maxLong" in form):
    # Use the supplied bounding box.
    minLat  = float(form['minLat'].value)
    minLong = float(form['minLong'].value)
    maxLat  = float(form['maxLat'].value)
    maxLong = float(form['maxLong'].value)
else:
    # Calculate the bounding box from the country outline.

    cursor.execute("SELECT " +
            "ST_YMin(ST_Envelope(outline))," +
            "ST_XMin(ST_Envelope(outline))," +
            "ST_YMax(ST_Envelope(outline))," +
            "ST_XMax(ST_Envelope(outline)) " +
            "FROM countries WHERE id=%s", (countryID,))

    row = cursor.fetchone()
    if row != None:
        minLat  = row[0]
        minLong = row[1]
        maxLat  = row[2]
        maxLong = row[3]
    else:
        print(HEADER)
        print('<b>Missing country</b>')
        print(FOOTER)
        sys.exit(0)

    minLong = minLong - 0.2
    minLat = minLat - 0.2
    maxLong = maxLong + 0.2
    maxLat = maxLat + 0.2

# Get the country's name.

cursor.execute("SELECT name FROM countries WHERE id=%s",
               (countryID,))
name = cursor.fetchone()[0]

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

# If necessary, zoom in.

if zoom != 0 and click_x != None and click_y != None:
    xFract = float(click_x)/float(mapWidth)
    longitude = minLong + xFract * (maxLong-minLong)

    yFract = float(click_y)/float(mapHeight)
    latitude = minLat + (1-yFract) * (maxLat-minLat)

    width = (maxLong - minLong) / (2**zoom)
    height = (maxLat - minLat) / (2**zoom)

    minLong = longitude - width / 2
    maxLong = longitude + width / 2
    minLat = latitude - height / 2
    maxLat = latitude + height / 2

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
print('<input type="image" src="' + imgFile + '" ismap ' +
      'onClick="return onClick()">')
print(HIDDEN_FIELD.format("countryID", countryID))
print(HIDDEN_FIELD.format("countryName", name))
print(HIDDEN_FIELD.format("zoom", zoom))
print(HIDDEN_FIELD.format("mapWidth", mapWidth))
print(HIDDEN_FIELD.format("mapHeight", mapHeight))
print(HIDDEN_FIELD.format("minLong", minLong))
print(HIDDEN_FIELD.format("minLat", minLat))
print(HIDDEN_FIELD.format("maxLong", maxLong))
print(HIDDEN_FIELD.format("maxLat", maxLat))
print('</form>')
print(FOOTER)

