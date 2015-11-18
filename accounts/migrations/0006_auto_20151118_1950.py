# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151118_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_history',
            field=models.ForeignKey(null=True, blank=True, to='accounts.AccountHistory'),
        ),
    ]
