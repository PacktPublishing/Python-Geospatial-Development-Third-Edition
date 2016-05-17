# import_gnis.py

import psycopg2
import os.path
import pyproj

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

cursor.execute("DELETE FROM places")

srcProj = pyproj.Proj(proj='longlat', ellps='GRS80',
                      datum='NAD83')
dstProj = pyproj.Proj(proj='longlat', ellps='WGS84',
                      datum='WGS84')

f = open(os.path.join("data",
                      "NationalFile_2015_0811.txt"), "r")
heading = f.readline() # Ignore field names.

num_inserted = 0

for line in f.readlines():
    parts = line.rstrip().split("|")
    featureName = parts[1]
    featureClass = parts[2]
    lat = float(parts[9])
    long = float(parts[10])

    if featureClass == "Populated Place":
        long,lat = pyproj.transform(srcProj, dstProj,
                                    long, lat)
        cursor.execute("INSERT INTO places " +
                       "(name, position) VALUES (%s, " +
                       "ST_SetSRID(" +
                       "ST_MakePoint(%s,%s), 4326))",
                       (featureName, long, lat))

        num_inserted = num_inserted + 1

        if num_inserted % 1000 == 0:
            connection.commit()

connection.commit()
f.close()

print("Inserted {} placenames".format(num_inserted))
