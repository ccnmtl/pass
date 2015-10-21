# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supportservices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportservicestate',
            name='services',
            field=models.ManyToManyField(to='supportservices.SupportService', blank=True),
        ),
    ]
