# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151118_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounthistory',
            options={'verbose_name_plural': 'Accounts History'},
        ),
    ]
