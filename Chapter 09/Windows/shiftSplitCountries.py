# shiftSplitCountries.py

import psycopg2
import shapely.wkt

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

countries_to_split = [] # List of (name,id,wkt) tuples.

cursor.execute("SELECT name,id,ST_AsText(outline) " +
               "FROM countries " +
               "WHERE (ST_XMin(outline::geometry) < -160) " +
               "AND (ST_XMax(outline::geometry) > 160)")
for row in cursor:
    countries_to_split.append(row)

for name,id,wkt in countries_to_split:
    print("Shifting outline for {}...".format(name))

    outline = shapely.wkt.loads(wkt)
    parts = []
    if outline.geom_type == "MultiPolygon":
        for part in outline.geoms:
            parts.append(part)
    else:
        print("This country doesn't have multiple parts!")
        continue

    # See how much land area is closer to -180 degrees, and how much is closer
    # to +180 degrees.  At the same time, we check to see if the country spans
    # the whole world (Antartica).  If so, we ignore it.

    area_on_left = 0
    area_on_right = 0
    spans_whole_world = False

    for part in parts:
        left  = part.bounds[0]
        right = part.bounds[2]
        if left == -180 and right == +180:
            spans_whole_world = True
            break

        distance_to_left_side = -(-180 - left)
        distance_to_right_side = 180 - right

        if distance_to_left_side < distance_to_right_side:
            area_on_left = area_on_left + part.area
        else:
            area_on_right = area_on_right + part.area

    if spans_whole_world:
        print("This country spans the whole world!")
        continue

    if area_on_left > area_on_right:
        print("  left")
    else:
        print("  right")

