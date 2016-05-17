import osgeo.ogr

shapefile = osgeo.ogr.Open("tl_2014_us_state.shp")
numLayers = shapefile.GetLayerCount()

print("Shapefile contains {} layers".format(numLayers))
print()

for layerNum in range(numLayers):
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()
    print("Layer {} has spatial reference {}".format(layerNum, spatialRef))
    print("Layer {} has {} features".format(layerNum, numFeatures))
    print()

    for featureNum in range(numFeatures):
        feature = layer.GetFeature(featureNum)
        featureName = feature.GetField("NAME")

        print("Feature {} has name {}".format(featureNum, featureName'))

