# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museris_data', '0002_person_personproperty'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataObjectPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=255, null=True, blank=True)),
                ('data_object', models.ForeignKey(related_name='people', to='museris_data.DataObject')),
                ('person', models.ForeignKey(related_name='objects', to='museris_data.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
