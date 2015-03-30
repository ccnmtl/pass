# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pagetree', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_location', models.CharField(default=b'/', max_length=255)),
                ('user', models.ForeignKey(related_name='application_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserVisited',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visited_time', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(to='pagetree.Section')),
                ('user', models.ForeignKey(to='main.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
