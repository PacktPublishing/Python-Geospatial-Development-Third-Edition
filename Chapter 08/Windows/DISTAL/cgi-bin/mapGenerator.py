# mapGenerator.py

import os, os.path, sys, tempfile

# NOTE: The following needs to be added to fix a problem with my path and
# Python3.  Remove to make this work generally.
sys.path.insert(0, "/usr/local/lib/python3.3/site-packages")
# End of fix.

import mapnik

def generateMap(tableName, minX, minY, maxX, maxY,
                mapWidth, mapHeight,
                hiliteExpr=None, points=None):

    extent = "{},{},{},{}".format(minX, minY, maxX, maxY)

    layer = mapnik.Layer("Layer")
    layer.datasource = mapnik.PostGIS(dbname="distal",
                                      table=tableName,
                                      user="distal_user",
                                      password="...",
                                      extent=extent,
                                      geometry_field="outline",
                                      srid=4326)

    map = mapnik.Map(mapWidth, mapHeight,
                     '+proj=longlat +datum=WGS84')
    map.background = mapnik.Color("#8080a0")

    style = mapnik.Style()

    rule = mapnik.Rule()
    if hiliteExpr != None:
        rule.filter = mapnik.Filter(hiliteExpr)

    rule.symbols.append(mapnik.PolygonSymbolizer(
        mapnik.Color("#408000")))
    rule.symbols.append(mapnik.LineSymbolizer(
        mapnik.Stroke(mapnik.Color("#000000"), 0.1)))

    style.rules.append(rule)

    rule = mapnik.Rule()
    rule.set_else(True)

    rule.symbols.append(mapnik.PolygonSymbolizer(
        mapnik.Color("#a0a0a0")))
    rule.symbols.append(mapnik.LineSymbolizer(
        mapnik.Stroke(mapnik.Color("#404040"), 0.1)))

    style.rules.append(rule)
    
    map.append_style("Map Style", style)
    layer.styles.append("Map Style")
    map.layers.append(layer)

    if points != None:
        memoryDatasource = mapnik.MemoryDatasource()
        context = mapnik.Context()
        context.push("name")
        next_id = 1
        for long,lat,name in points:
            wkt = "POINT (%0.8f %0.8f)" % (long,lat)
            feature = mapnik.Feature(context, next_id)
            feature['name'] = name
            feature.add_geometries_from_wkt(wkt)
            next_id = next_id + 1
            memoryDatasource.add_feature(feature)

        layer = mapnik.Layer("Points")
        layer.datasource = memoryDatasource

        style = mapnik.Style()
        rule = mapnik.Rule()

        pointImgFile = os.path.join(os.path.dirname(__file__),
                                    "point.png")

        shield = mapnik.ShieldSymbolizer(
                   mapnik.Expression('[name]'),
                   "DejaVu Sans Bold", 10,
                   mapnik.Color("#000000"),
                   mapnik.PathExpression(pointImgFile))
        shield.displacement = (0, 7)
        shield.unlock_image = True
        rule.symbols.append(shield)

        style.rules.append(rule)

        map.append_style("Point Style", style)
        layer.styles.append("Point Style")

        map.layers.append(layer)

    map.zoom_to_box(mapnik.Envelope(minX, minY, maxX, maxY))

    scriptDir = os.path.dirname(__file__)
    cacheDir = os.path.join(scriptDir, "..", "mapCache")
    if not os.path.exists(cacheDir):
        os.mkdir(cacheDir)
    fd,filename = tempfile.mkstemp(".png", dir=cacheDir)
    os.close(fd)

    mapnik.render_to_file(map, filename, "png")

    return "../mapCache/" + os.path.basename(filename)
