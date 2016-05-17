# calcBoundingBoxes.py

from osgeo import ogr

shapefile = ogr.Open("TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

countries = [] # List of (code, name, minLat, maxLat,
               # minLong, maxLong) tuples.

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    countryCode = feature.GetField("ISO3")
    countryName = feature.GetField("NAME")
    geometry = feature.GetGeometryRef()
    minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()

    countries.append((countryName, countryCode,
                      minLat, maxLat, minLong, maxLong))

countries.sort()

for name,code,minLat,maxLat,minLong,maxLong in countries:
    print("{} ({}) lat={:.4f}..{:.4f},long={:.4f}..{:.4f}"
          .format(name,code,minLat,maxLat,minLong,maxLong))

