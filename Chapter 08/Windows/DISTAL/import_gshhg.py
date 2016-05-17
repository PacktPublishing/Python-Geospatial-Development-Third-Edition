# import_gshhg.py

import os.path
import psycopg2
import osgeo.ogr

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

cursor.execute("DELETE FROM shorelines")

for level in [1, 2, 3, 4]:
    num_done = 0

    srcFile = os.path.join("data", "GSHHS_shp", "f",
                           "GSHHS_f_L{}.shp".format(level))
    shapefile = osgeo.ogr.Open(srcFile)
    layer = shapefile.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        geometry = feature.GetGeometryRef()
        if geometry.IsValid():
            cursor.execute("INSERT INTO shorelines " +
                           "(level,outline) VALUES " +
                           "(%s, ST_GeometryFromText(%s, 4326))",
                           (level, geometry.ExportToWkt()))

        num_done = num_done + 1

    connection.commit()

    print("Imported {} shorelines at level {}".format(num_done, level))

