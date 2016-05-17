# Sample program to write raster-format data.

# Create our file:

from osgeo import gdal
driver = gdal.GetDriverByName("GTiff")
dstFile = driver.Create("Example Raster.tiff", 360, 180, 1, gdal.GDT_Int16)

# Define the projection:

from osgeo import osr
spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84")
dstFile.SetProjection(spatialReference.ExportToWkt())

# Set the georeferencing transform:

originX    = -180
originY    = 90
cellWidth  = 1.0
cellHeight = 1.0

dstFile.SetGeoTransform([originX, cellWidth, 0,
                         originY, 0, -cellHeight])

# Get the raster band:

band = dstFile.GetRasterBand(1)

# Generate the random values to store:

import random

values = []
for row in range(180):
    row_data = []
    for col in range(360):
        row_data.append(random.randint(1, 100))
    values.append(row_data)

# Write our data using "struct":

import struct

fmt = "<" + ("h" * band.XSize)

for row in range(180):
    scanline = struct.pack(fmt, *values[row])
    band.WriteRaster(0, row, 360, 1, scanline)

# Alternatively, write our data using NumPy:

#import numpy
#
#array = numpy.array(values, dtype=numpy.int16)
#band.WriteArray(array)

