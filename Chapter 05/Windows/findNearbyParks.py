# findNearbyParks.py

from osgeo import ogr
import shapely.geometry
import shapely.wkt

MAX_DISTANCE = 0.1 # Angular distance; approx 10 km.

print("Loading urban areas...")

urbanAreas = {} # Maps area name to Shapely polygon.

shapefile = ogr.Open("tl_2015_us_cbsa.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    print("Dilating feature {} of {}".format(i, layer.GetFeatureCount()))
    feature = layer.GetFeature(i)
    name = feature.GetField("NAME")
    geometry = feature.GetGeometryRef()
    outline = shapely.wkt.loads(geometry.ExportToWkt())
    dilatedOutline = outline.buffer(MAX_DISTANCE)
    urbanAreas[name] = dilatedOutline

print("Checking parks...")

f = open("CA_Features_XXXX.txt", "r")
for line in f.readlines():
    chunks = line.rstrip().split("|")
    if chunks[2] == "Park":
        parkName = chunks[1]
        latitude = float(chunks[9])
        longitude = float(chunks[10])

        pt = shapely.geometry.Point(longitude, latitude)

        for urbanName,urbanArea in urbanAreas.items():
            if urbanArea.contains(pt):
                print("{} is in or near {}"
                      .format(parkName, urbanName))
f.close()

