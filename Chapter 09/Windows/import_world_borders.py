# import_world_borders.py

# DELETE FROM countries;
# ALTER TABLE countries DROP COLUMN outline;
# ALTER TABLE countries ADD COLUMN outline GEOMETRY(GEOMETRY, 4326);

import os.path
import psycopg2
import osgeo.ogr

import shapely.wkt
from shapely.geometry import MultiPolygon
from shapely.affinity import translate

#############################################################################

def adjust_for_antimeridian(name, wkt):
    """ Adjust the given country if it crosses the anti-meridian line.

        We return the country's original or adjusted outline, in wkt format.
    """
    outline = shapely.wkt.loads(wkt)

    # Ignore the country if it doesn't have multiple parts.

    if outline.geom_type != "MultiPolygon":
        print("Importing {}".format(name))
        return wkt

    # Ignore the country if it doesn't sit close to the anti-meridian line on
    # both the left and right sides.

    minLong,minLat,maxLong,maxLat = outline.bounds
    if minLong >= -160 or maxLong <= 160:
        print("Importing {}".format(name))
        return wkt # No need to adjust.

    # Split the country up into individual parts, recording whether each part
    # is closer to the anti-meridian line on the left side or the right side.

    parts = [] # List of parts.  Each entry is a dictionary with 'side' and
               # 'geom' entries.

    for geom in outline.geoms:
        left = geom.bounds[0]
        right = geom.bounds[2]
        if left == -180 and right == +180:
            print("{} spans the entire world, so we can't shift it."
                  .format(name))
            return wkt

        distance_to_left_side = -(-180 - left)
        distance_to_right_side = 180 - right

        if distance_to_left_side < distance_to_right_side:
            side = "left"
        else:
            side = "right"

        parts.append({'side' : side,
                      'geom' : geom})

    # Decide whether to shift the country to the left side or the right side of
    # the world map.  We do this based on the number of parts on each side.

    num_on_left = 0
    num_on_right = 0

    for part in parts:
        if part['side'] == "left":
            num_on_left = num_on_left + 1
        else:
            num_on_right = num_on_right + 1

    if num_on_left > num_on_right:
        print("Shifting {} to left".format(name))
        shift_direction = "left"
    else:
        print("Shifting {} to right".format(name))
        shift_direction = "right"

    # Shift the parts.

    for part in parts:
        old_bounds = part['geom'].bounds
        if part['side'] == "left" and shift_direction == "right":
            part['geom'] = translate(part['geom'], 360)
        elif part['side'] == "right" and shift_direction == "left":
            part['geom'] = translate(part['geom'], -360)

    # Combine the translated parts back into a MultiPolygon.

    polygons = []
    for part in parts:
        polygons.append(part['geom'])
    combined = MultiPolygon(polygons)

    return combined.wkt

#############################################################################

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

cursor.execute("DELETE FROM countries")

srcFile = os.path.join("data", "TM_WORLD_BORDERS-0.3",
                       "TM_WORLD_BORDERS-0.3.shp")
shapefile = osgeo.ogr.Open(srcFile)
layer = shapefile.GetLayer(0)
num_done = 0

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    name = feature.GetField("NAME")
    wkt = feature.GetGeometryRef().ExportToWkt()

    wkt = adjust_for_antimeridian(name, wkt)

    cursor.execute("INSERT INTO countries (name,outline) " +
                   "VALUES (%s, ST_GeometryFromText(%s, 4326))",
                   (name, wkt))

    num_done = num_done + 1

connection.commit()


print("Imported {} countries".format(num_done))

