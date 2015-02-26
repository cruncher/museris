# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import museris_data.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataObject',
            fields=[
                ('object_id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataObjectImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=museris_data.models.image_upload_to, blank=True)),
                ('image_url', models.URLField(null=True, blank=True)),
                ('data_object', models.ForeignKey(related_name='images', to='museris_data.DataObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataObjectLatLong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=15, decimal_places=12)),
                ('longitude', models.DecimalField(max_digits=15, decimal_places=12)),
                ('data_object', models.ForeignKey(related_name='coords', to='museris_data.DataObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataObjectProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('value', models.CharField(db_index=True, max_length=1024, null=True, blank=True)),
                ('data_object', models.ForeignKey(related_name='properties', to='museris_data.DataObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dataobject',
            name='institution',
            field=models.ForeignKey(related_name='data_objects', to='museris_data.Institution'),
            preserve_default=True,
        ),
    ]
