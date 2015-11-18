# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151118_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='region',
            field=models.CharField(choices=[('eu', 'Europe'), ('us', 'Americas'), ('kr', 'Korea'), ('tw', 'Taiwan')], max_length=2),
        ),
    ]
