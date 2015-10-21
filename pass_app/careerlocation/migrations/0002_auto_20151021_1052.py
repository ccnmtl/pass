# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('careerlocation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='questions',
            field=models.ManyToManyField(to='careerlocation.ActorQuestion', blank=True),
        ),
        migrations.AlterField(
            model_name='careerlocationstate',
            name='actors',
            field=models.ManyToManyField(to='careerlocation.Actor', blank=True),
        ),
        migrations.AlterField(
            model_name='careerlocationstate',
            name='layers',
            field=models.ManyToManyField(to='careerlocation.MapLayer', blank=True),
        ),
        migrations.AlterField(
            model_name='careerlocationstate',
            name='responses',
            field=models.ManyToManyField(to='careerlocation.ActorResponse', blank=True),
        ),
        migrations.AlterField(
            model_name='careerlocationstate',
            name='strategies_viewed',
            field=models.ManyToManyField(related_name='strategies_viewed', to='careerlocation.Strategy', blank=True),
        ),
        migrations.AlterField(
            model_name='careerlocationstate',
            name='strategy_responses',
            field=models.ManyToManyField(related_name='strategy_responses', to='careerlocation.ActorResponse', blank=True),
        ),
    ]
