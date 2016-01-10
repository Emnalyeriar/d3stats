# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0003_auto_20160109_1905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hero',
            options={'verbose_name_plural': 'Heroes'},
        ),
        migrations.AlterModelOptions(
            name='herohistory',
            options={'verbose_name_plural': 'Heroes History'},
        ),
        migrations.RenameField(
            model_name='herohistory',
            old_name='critDamage',
            new_name='crit_damage',
        ),
    ]
