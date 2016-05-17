# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField()),
                ('width', models.IntegerField()),
                ('precision', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('value', models.CharField(max_length=255, blank=True, null=True)),
                ('attribute', models.ForeignKey(to='shared.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('geom_point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('geom_multipoint', django.contrib.gis.db.models.fields.MultiPointField(blank=True, null=True, srid=4326)),
                ('geom_multilinestring', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=4326)),
                ('geom_multipolygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('geom_geometrycollection', django.contrib.gis.db.models.fields.GeometryCollectionField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Shapefile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('filename', models.CharField(max_length=255)),
                ('srs_wkt', models.CharField(max_length=255)),
                ('geom_type', models.CharField(max_length=50)),
                ('encoding', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='feature',
            name='shapefile',
            field=models.ForeignKey(to='shared.Shapefile'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='feature',
            field=models.ForeignKey(to='shared.Feature'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='shapefile',
            field=models.ForeignKey(to='shared.Shapefile'),
        ),
    ]
