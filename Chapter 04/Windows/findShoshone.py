# findShoshone.py

import pyproj

distance = 132.7 * 1000
angle    = 270.0

f = open("CA_Features_XXXX.txt", "r")
for line in f.readlines():
    chunks = line.rstrip().split("|")
    if chunks[1] == "Shoshone" and \
       chunks[2] == "Populated Place" and \
       chunks[3] == "CA":
        latitude = float(chunks[9])
        longitude = float(chunks[10])

        geod = pyproj.Geod(ellps='WGS84')
        newLong,newLat,invAngle = geod.fwd(longitude,
                                           latitude,
                                           angle, distance)

        print("Shoshone is at {:.4f},{:.4f}"
              .format(latitude, longitude))
        print("The point {:.2f} km west of Shoshone "
              .format(distance/1000.0) +
              "is at {:.4f}, {:.4f}".format(newLat, newLong))

f.close()

