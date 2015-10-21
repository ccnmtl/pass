# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infographic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infographicstate',
            name='items',
            field=models.ManyToManyField(to='infographic.InfographicItem', blank=True),
        ),
    ]
