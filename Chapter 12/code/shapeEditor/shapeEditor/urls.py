from django.conf.urls import include, url
from django.contrib.gis import admin
import shapeEditor.shapefiles.views

urlpatterns = [
    url(r'^$', shapeEditor.shapefiles.views.list_shapefiles),
    url(r'^import$', shapeEditor.shapefiles.views.import_shapefile),
    url(r'^export/(?P<shapefile_id>\d+)$',
            shapeEditor.shapefiles.views.export_shapefile),
    url(r'^admin/', include(admin.site.urls)),
]
