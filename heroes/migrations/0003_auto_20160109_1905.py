# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0002_auto_20160109_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='legendary_powers',
        ),
        migrations.AddField(
            model_name='hero',
            name='legendary_powers',
            field=models.ManyToManyField(to='heroes.LegendaryPower'),
        ),
    ]
