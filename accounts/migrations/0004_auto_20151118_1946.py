# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151116_2230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounthistory',
            old_name='account',
            new_name='related_account',
        ),
        migrations.AddField(
            model_name='account',
            name='last_history',
            field=models.ForeignKey(default=None, to='accounts.AccountHistory'),
        ),
    ]
