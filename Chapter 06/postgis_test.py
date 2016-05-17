import psycopg2
from osgeo import ogr

# Connect to the database.

connection = psycopg2.connect(database="...", user="...",
                              password="...")
cursor = connection.cursor()

# Create the database table.

cursor.execute("DROP TABLE IF EXISTS borders")
cursor.execute("CREATE TABLE borders (" +
               "id SERIAL PRIMARY KEY," +
               "name VARCHAR NOT NULL," +
               "iso_code VARCHAR NOT NULL," +
               "outline GEOGRAPHY)")
cursor.execute("CREATE INDEX border_index ON borders USING GIST(outline)")
connection.commit()

# Import the world borders dataset.

shapefile = ogr.Open("TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature  = layer.GetFeature(i)
    name     = feature.GetField("NAME")
    iso_code = feature.GetField("ISO3")
    geometry = feature.GetGeometryRef()
    wkt      = geometry.ExportToWkt()

    cursor.execute("INSERT INTO borders (name, iso_code, outline) " +
                   "VALUES (%s, %s, ST_GeogFromText(%s))",
                   (name, iso_code, wkt))

connection.commit()

# Perform a spatial query.

start_long = 8.542
start_lat  = 47.377
radius     = 500000

cursor.execute("SELECT name FROM borders WHERE ST_DWITHIN(" +
               "ST_MakePoint(%s, %s), outline, %s)",
               (start_long, start_lat, radius))
for row in cursor:
    print(row[0])

