# tileShorelines.py

import math

import pyproj
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
import shapely.wkt
import psycopg2

MAX_DISTANCE = 100000 # Maximum search radius, in metres.

#############################################################################

def expandRect(minLat, minLong, maxLat, maxLong, distance):
    geod = pyproj.Geod(ellps="WGS84")
    midLat  = (minLat + maxLat) / 2.0
    midLong = (minLong + maxLong) / 2.0

    try:
        availDistance = geod.inv(midLong, maxLat, midLong,
                                 +90)[2]
        if availDistance >= distance:
            x,y,angle = geod.fwd(midLong, maxLat, 0, distance)
            maxLat = y
        else:
            maxLat = +90
    except:
        maxLat = +90 # Can't expand north.

    try:
        availDistance = geod.inv(maxLong, midLat, +180,
                                 midLat)[2]
        if availDistance >= distance:
            x,y,angle = geod.fwd(maxLong, midLat, 90,
                                 distance)
            maxLong = x
        else:
            maxLong = +180
    except:
        maxLong = +180 # Can't expand east.

    try:
        availDistance = geod.inv(midLong, minLat, midLong,
                                 -90)[2]
        if availDistance >= distance:
            x,y,angle = geod.fwd(midLong, minLat, 180,
                                 distance)
            minLat = y
        else:
            minLat = -90
    except:
        minLat = -90 # Can't expand south.

    try:
        availDistance = geod.inv(maxLong, midLat, -180,
                                 midLat)[2]
        if availDistance >= distance:
            x,y,angle = geod.fwd(minLong, midLat, 270,
                                 distance)
            minLong = x
        else:
            minLong = -180
    except:
        minLong = -180 # Can't expand west.

    return (minLat, minLong, maxLat, maxLong)

#############################################################################

print("Opening database connection...")

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

print("Loading shoreline polygons...")

shorelines = []

cursor.execute("SELECT ST_AsText(outline) " +
               "FROM shorelines WHERE level=1")

for row in cursor:
    outline = shapely.wkt.loads(row[0])
    shorelines.append(outline)

print("Tiling polygons...")

tilePolys = []
for iLat in range(-90, +90):
    tilePolys.append([])
    for iLong in range(-180, +180):
        tilePolys[-1].append([])

for n,shoreline in enumerate(shorelines):
    print("Splitting polygon {} of {}...".format(n+1, len(shorelines)))

    minLong,minLat,maxLong,maxLat = shoreline.bounds
    minLong = int(math.floor(minLong))
    minLat  = int(math.floor(minLat))
    maxLong = int(math.ceil(maxLong))
    maxLat  = int(math.ceil(maxLat))

    vStrips = []
    for iLong in range(minLong, maxLong+1):
        print("  Creating strip {} of {}".format(iLong-minLong+1,
                                                 maxLong-minLong+1))

        stripMinLat  = minLat
        stripMaxLat  = maxLat
        stripMinLong = iLong
        stripMaxLong = iLong + 1

        bMinLat,bMinLong,bMaxLat,bMaxLong = \
                expandRect(stripMinLat, stripMinLong,
                           stripMaxLat, stripMaxLong,
                           MAX_DISTANCE)

        bounds = Polygon([(bMinLong, bMinLat),
                          (bMinLong, bMaxLat),
                          (bMaxLong, bMaxLat),
                          (bMaxLong, bMinLat),
                          (bMinLong, bMinLat)])

        strip = shoreline.intersection(bounds)
        vStrips.append(strip)

    stripNum = 0
    for iLong in range(minLong, maxLong+1):
        print("  Splitting strip {} of {}".format(iLong-minLong+1,
                                                  maxLong-minLong+1))
        vStrip = vStrips[stripNum]
        stripNum = stripNum + 1

        for iLat in range(minLat, maxLat+1):
            bMinLat,bMinLong,bMaxLat,bMaxLong = \
                expandRect(iLat, iLong, iLat+1, iLong+1,
                           MAX_DISTANCE)

            bounds = Polygon([(bMinLong, bMinLat),
                              (bMinLong, bMaxLat),
                              (bMaxLong, bMaxLat),
                              (bMaxLong, bMinLat),
                              (bMinLong, bMinLat)])

            polygon = vStrip.intersection(bounds)
            if not polygon.is_empty:
                tilePolys[iLat][iLong].append(polygon)

print("Creating database table...")

cursor.execute("DROP TABLE IF EXISTS tiled_shorelines")
cursor.execute("CREATE TABLE tiled_shorelines (" +
               "  intLat  INTEGER," +
               "  intLong INTEGER," +
               "  outline GEOMETRY(GEOMETRY, 4326)," +
               "  PRIMARY KEY (intLat, intLong))")
cursor.execute("CREATE INDEX tiledShorelineIndex "+
               "ON tiled_shorelines USING GIST(outline)")

for iLat in range(-90, +90):
    print("Saving tiles at latitude {}".format(iLat))

    for iLong in range(-180, +180):
        polygons = tilePolys[iLat][iLong]
        if len(polygons) == 0:
            outline = Polygon()
        else:
            outline = shapely.ops.cascaded_union(polygons)
        wkt = shapely.wkt.dumps(outline)

        cursor.execute("INSERT INTO tiled_shorelines " +
                        "(intLat, intLong, outline) " +
                        "VALUES (%s, %s, " +
                        "ST_GeomFromText(%s))",
                        (iLat, iLong, wkt))
    connection.commit()

connection.close()

