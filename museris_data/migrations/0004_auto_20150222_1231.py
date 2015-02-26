# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museris_data', '0003_dataobjectperson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'People'},
        ),
        migrations.AlterField(
            model_name='dataobjectperson',
            name='person',
            field=models.ForeignKey(related_name='data_objects', to='museris_data.Person'),
            preserve_default=True,
        ),
    ]
