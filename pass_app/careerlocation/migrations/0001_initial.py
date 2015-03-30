# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=2, choices=[(b'IV', b'Interview Stakeholders'), (b'LC', b'Select Practice Location'), (b'BD', b'Complete Board Application'), (b'RP', b'Practice Location Report'), (b'DS', b'Defend Strategy')])),
                ('profile', models.TextField(null=True, blank=True)),
                ('left', models.IntegerField(null=True, blank=True)),
                ('top', models.IntegerField(null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=b'layers/%Y/%m/%d/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActorQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('answer', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['question'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActorResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('long_response', models.TextField(null=True, blank=True)),
                ('actor', models.ForeignKey(to='careerlocation.Actor')),
                ('question', models.ForeignKey(to='careerlocation.ActorQuestion')),
                ('user', models.ForeignKey(related_name='actor_state_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CareerLocationBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view', models.CharField(max_length=2, choices=[(b'IV', b'Interview Stakeholders'), (b'LC', b'Select Practice Location'), (b'BD', b'Complete Board Application'), (b'RP', b'Practice Location Report'), (b'DS', b'Defend Strategy')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CareerLocationState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('practice_location_row', models.IntegerField(null=True, blank=True)),
                ('practice_location_column', models.IntegerField(null=True, blank=True)),
                ('actors', models.ManyToManyField(to='careerlocation.Actor', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CareerLocationStrategyBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view', models.CharField(max_length=2, choices=[(b'VS', b'View Strategies'), (b'SS', b'Select Strategy'), (b'DS', b'Defend Strategy Selection'), (b'PC', b'Strategy Pros And Cons'), (b'RS', b'Rethink Strategy Selection')])),
                ('instructions', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CareerLocationSummaryBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=255)),
                ('legend', models.TextField(null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=b'layers/%Y/%m/%d/', blank=True)),
                ('z_index', models.IntegerField(default=999)),
                ('transparency', models.IntegerField(default=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordinal', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=256)),
                ('summary', models.TextField()),
                ('pros', models.TextField()),
                ('cons', models.TextField()),
                ('pdf', models.FileField(null=True, upload_to=b'pdf/', blank=True)),
                ('example', models.URLField(null=True, blank=True)),
                ('question', models.ForeignKey(blank=True, to='careerlocation.ActorQuestion', null=True)),
            ],
            options={
                'ordering': ['ordinal'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='careerlocationstrategyblock',
            name='base_layer',
            field=models.ForeignKey(to='careerlocation.MapLayer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstrategyblock',
            name='optional_layers',
            field=models.ManyToManyField(related_name='strategy_optional_layers', to='careerlocation.MapLayer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstrategyblock',
            name='questioner',
            field=models.ForeignKey(blank=True, to='careerlocation.Actor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstate',
            name='layers',
            field=models.ManyToManyField(to='careerlocation.MapLayer', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstate',
            name='responses',
            field=models.ManyToManyField(to='careerlocation.ActorResponse', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstate',
            name='strategies_viewed',
            field=models.ManyToManyField(related_name='strategies_viewed', null=True, to='careerlocation.Strategy', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstate',
            name='strategy_responses',
            field=models.ManyToManyField(related_name='strategy_responses', null=True, to='careerlocation.ActorResponse', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstate',
            name='strategy_selected',
            field=models.ForeignKey(related_name='strategy_selected', blank=True, to='careerlocation.Strategy', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationstate',
            name='user',
            field=models.ForeignKey(related_name='career_location_state', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationblock',
            name='base_layer',
            field=models.ForeignKey(to='careerlocation.MapLayer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='careerlocationblock',
            name='optional_layers',
            field=models.ManyToManyField(related_name='optional_layers', to='careerlocation.MapLayer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actor',
            name='questions',
            field=models.ManyToManyField(to='careerlocation.ActorQuestion', null=True, blank=True),
            preserve_default=True,
        ),
    ]
