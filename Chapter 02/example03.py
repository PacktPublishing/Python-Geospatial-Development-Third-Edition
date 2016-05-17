import osgeo.ogr

def analyzeGeometry(geometry, indent=0):
    s = []
    s.append("  " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    if geometry.GetGeometryCount() > 0:
        s.append(" containing:")

    print("".join(s))

    for i in range(geometry.GetGeometryCount()):
        analyzeGeometry(geometry.GetGeometryRef(i), indent+1)

shapefile = osgeo.ogr.Open("tl_2014_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(12)
geometry = feature.GetGeometryRef()

analyzeGeometry(geometry)
