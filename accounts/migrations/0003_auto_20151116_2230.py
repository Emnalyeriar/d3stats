# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151114_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='region',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='accounthistory',
            name='account',
            field=models.ForeignKey(to='accounts.Account', related_name='history'),
        ),
    ]
