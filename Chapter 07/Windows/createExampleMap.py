# createExampleMap.py

import mapnik

MIN_LAT  = -35
MAX_LAT  = +35
MIN_LONG = -12
MAX_LONG = +50

MAP_WIDTH  = 700
MAP_HEIGHT = 800

# Define our polygon styles:

polygonStyle = mapnik.Style()

rule = mapnik.Rule()
rule.filter = mapnik.Filter("[NAME] = 'Angola'")
symbol = mapnik.PolygonSymbolizer(mapnik.Color("#604040"))
rule.symbols.append(symbol)

polygonStyle.rules.append(rule)

rule = mapnik.Rule()
rule.filter = mapnik.Filter("[NAME] != 'Angola'")
symbol = mapnik.PolygonSymbolizer(mapnik.Color("#406040"))
rule.symbols.append(symbol)

polygonStyle.rules.append(rule)

rule = mapnik.Rule()
symbol = mapnik.LineSymbolizer(mapnik.Color("#000000"), 0.1)
rule.symbols.append(symbol)

polygonStyle.rules.append(rule)

# Define our label style:

labelStyle = mapnik.Style()

rule = mapnik.Rule()
symbol = mapnik.TextSymbolizer(mapnik.Expression("[NAME]"),
                               "DejaVu Sans Book", 12,
                               mapnik.Color("#000000"))
rule.symbols.append(symbol)

labelStyle.rules.append(rule)

# Setup our datasource:

datasource = mapnik.Shapefile(file="TM_WORLD_BORDERS-0.3/" +
                                   "TM_WORLD_BORDERS-0.3.shp")

# Define our map layers:

polygonLayer = mapnik.Layer("Polygons")
polygonLayer.datasource = datasource
polygonLayer.styles.append("PolygonStyle")

labelLayer = mapnik.Layer("Labels")
labelLayer.datasource = datasource
labelLayer.styles.append("LabelStyle")

# Setup our Map object:

map = mapnik.Map(MAP_WIDTH, MAP_HEIGHT,
                 "+proj=longlat +datum=WGS84")
map.background = mapnik.Color("#8080a0")

map.append_style("PolygonStyle", polygonStyle)
map.append_style("LabelStyle",   labelStyle)

map.layers.append(polygonLayer)
map.layers.append(labelLayer)

map.zoom_to_box(mapnik.Box2d(MIN_LONG, MIN_LAT,
                             MAX_LONG, MAX_LAT))
mapnik.render_to_file(map, "map.png")


