# Sample program to read raster-format data.

from osgeo import gdal

srcFile = gdal.Open("Example Raster.tiff")
band = srcFile.GetRasterBand(1)

# Read our data using "struct":

import struct

fmt = "<" + ("h" * band.XSize)

for row in range(band.YSize):
    scanline = band.ReadRaster(0, row, band.XSize, 1,
                               band.XSize, 1,
                               band.DataType)
    row_data = struct.unpack(fmt, scanline)
    print(row_data)

# Alternatively, read the data using NumPy:

values = band.ReadAsArray()
for row in range(band.XSize):
    print(values[row])

