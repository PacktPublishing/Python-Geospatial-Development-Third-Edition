# import_world_borders.py

import os.path
import psycopg2
import osgeo.ogr

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

    cursor.execute("INSERT INTO countries (name,outline) " +
                   "VALUES (%s, ST_GeometryFromText(%s, 4326))",
                   (name, wkt))

    num_done = num_done + 1

connection.commit()

print("Imported {} countries".format(num_done))

