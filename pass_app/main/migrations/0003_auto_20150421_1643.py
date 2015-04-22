# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150421_1635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uservisited',
            old_name='user',
            new_name='profile',
        ),
    ]
