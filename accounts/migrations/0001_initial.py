# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('battle_tag', models.CharField(max_length=100)),
                ('last_updated', models.DateField(auto_now=True)),
                ('last_played', models.DateField()),
                ('heroes', jsonfield.fields.JSONField()),
                ('paragon_sc', models.IntegerField()),
                ('paragon_hc', models.IntegerField()),
                ('paragon_sc_s', models.IntegerField()),
                ('paragon_hc_s', models.IntegerField()),
                ('guild_name', models.CharField(max_length=200)),
                ('time_played', jsonfield.fields.JSONField()),
                ('monsters', models.IntegerField()),
                ('elites', models.IntegerField()),
                ('monsters_hc', models.IntegerField()),
            ],
        ),
    ]
