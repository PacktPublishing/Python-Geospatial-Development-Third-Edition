import osgeo.ogr

shapefile = osgeo.ogr.Open("tl_2014_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(12)

print("Feature 12 has the following attributes:")
print()

attributes = feature.items()

for key,value in attributes.items():
    print(" {} = {}".format(key, value))

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()

print()
print("Feature's geometry data consists of a {}".format(geometryName))

