# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museris_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('object_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('value', models.CharField(db_index=True, max_length=1024, null=True, blank=True)),
                ('person', models.ForeignKey(related_name='properties', to='museris_data.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
