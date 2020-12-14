## $5 Tech Unlocked 2021!
[Buy and download this product for only $5 on PacktPub.com](https://www.packtpub.com/)
-----
*The $5 campaign         runs from __December 15th 2020__ to __January 13th 2021.__*

#Python Geospatial Development-Third Edition


This is the code repository for [Python Geospatial Development-Third Edition](https://www.packtpub.com/application-development/python-geospatial-development-third-edition?utm_source=GitHub&utm_medium=Repository&utm_campaign=9781785288937), published by Packt. It contains all the supporting project files necessary to work through the book from start to finish.

##Instructions and Navigation

The code included with this book is meant for use as an aid in performing the exercises and should not be used as a replacement for the book itself.
Used out of context, the code may result in an unusable configuration and no warranty is given.

The code will look like the following:
```
import math

lat1 = 42.0095
long1 = -122.3782

lat2 = 32.5288
long2 = -117.2049

rLat1 = math.radians(lat1)
rLong1 = math.radians(long1)
rLat2 = math.radians(lat2)
rLong2 = math.radians(long2)

dLat = rLat2 - rLat1
dLong = rLong2 - rLong1
a = math.sin(dLat/2)**2 + math.cos(rLat1) * math.cos(rLat2) \
                        * math.sin(dLong/2)**2
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
distance = 6371 * c

print("Great circle distance is {:0.0f} kilometers".format(
      distance))


```


##Related OpenStack Products:
* [Python GeoSpatial Development](https://www.packtpub.com/application-development/python-geospatial-development)
* [Python Geospatial Development - Second Edition](https://www.packtpub.com/application-development/python-geospatial-development-second-edition)
* [Learning Geospatial Analysis with Python](https://www.packtpub.com/application-development/learning-geospatial-analysis-python)

