# import_geonames.py

import psycopg2
import os.path

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

f = open(os.path.join("data", "Countries.txt"), "r")

heading = f.readline() # Ignore field names.

num_inserted = 0

for line in f:
    parts = line.rstrip().split("\t")
    lat = float(parts[3])
    long = float(parts[4])
    featureClass = parts[9]
    featureDesignation = parts[10]
    nameType = parts[17]
    featureName = parts[22]

    if (featureClass == "P" and nameType == "N" and
        featureDesignation in ["PPL", "PPLA", "PPLC"]):
        cursor.execute("INSERT INTO places " +
                       "(name, position) VALUES (%s, " +
                       "ST_SetSRID(" +
                       "ST_MakePoint(%s,%s), 4326))",
                       (featureName, long, lat))

        num_inserted = num_inserted + 1
        if num_inserted % 1000 == 0:
            connection.commit()

f.close()
connection.commit()

print("Inserted {} placenames".format(num_inserted))
