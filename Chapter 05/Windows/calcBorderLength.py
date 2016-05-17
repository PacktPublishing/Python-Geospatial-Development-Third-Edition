import sys
from osgeo import ogr, osr
import pyproj

def getLineSegmentsFromGeometry(geometry):
    segments = []
    if geometry.GetPointCount() > 0:
        segment = []
        for i in range(geometry.GetPointCount()):
            segment.append(geometry.GetPoint_2D(i))
        segments.append(segment)
    for i in range(geometry.GetGeometryCount()):
        subGeometry = geometry.GetGeometryRef(i)
        segments.extend(
            getLineSegmentsFromGeometry(subGeometry))
    return segments

if len(sys.argv) != 2:
    print("Usage: calcFeatureLengths.py <shapefile>")
    sys.exit(1)

filename = sys.argv[1]

shapefile = ogr.Open(filename)
layer = shapefile.GetLayer(0)
spatialRef = layer.GetSpatialRef()
if spatialRef == None:
    print("Shapefile lacks a spatial reference, using WGS84.")
    spatialRef = osr.SpatialReference()
    spatialRef.SetWellKnownGeogCS('WGS84')

if spatialRef.IsProjected():
    srcProj = pyproj.Proj(spatialRef.ExportToProj4())
    dstProj = pyproj.Proj(proj='longlat', ellps='WGS84',
                          datum='WGS84')

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = feature.GetGeometryRef()
    segments = getLineSegmentsFromGeometry(geometry)

    geod = pyproj.Geod(ellps='WGS84')

    totLength = 0.0
    for segment in segments:
        for j in range(len(segment)-1):
            pt1 = segment[j]
            pt2 = segment[j+1]

            long1,lat1 = pt1
            long2,lat2 = pt2

            if spatialRef.IsProjected():
                long1,lat1 = pyproj.transform(srcProj,
                                              dstProj,
                                              long1, lat1)
                long2,lat2 = pyproj.transform(srcProj,
                                              dstProj,
                                              long2, lat2)

            try:
                angle1,angle2,distance = geod.inv(long1, lat1,
                                                  long2, lat2)
            except ValueError:
                print("Unable to calculate distance from "
                      + "{:.4f},{:.4f} to {:.4f},{:.4f}"
                        .format(long1, lat1, long2, lat2))
                distance = 0.0

            totLength += distance

    print("Total length of feature {} is {:.2f} km"
          .format(i, totLength/1000))

