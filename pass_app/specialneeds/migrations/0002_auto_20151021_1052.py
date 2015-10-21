# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specialneeds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialneedscallstate',
            name='questions',
            field=models.ManyToManyField(to='specialneeds.SpecialNeedsCall', blank=True),
        ),
    ]
