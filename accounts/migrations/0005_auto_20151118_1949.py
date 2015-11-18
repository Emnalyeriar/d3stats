# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151118_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_history',
            field=models.ForeignKey(to='accounts.AccountHistory', blank=True),
        ),
    ]
