# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('paragon_sc', models.IntegerField()),
                ('paragon_hc', models.IntegerField()),
                ('paragon_sc_s', models.IntegerField()),
                ('paragon_hc_s', models.IntegerField()),
                ('monsters', models.IntegerField()),
                ('elites', models.IntegerField()),
                ('monsters_hc', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='elites',
        ),
        migrations.RemoveField(
            model_name='account',
            name='monsters',
        ),
        migrations.RemoveField(
            model_name='account',
            name='monsters_hc',
        ),
        migrations.RemoveField(
            model_name='account',
            name='paragon_hc',
        ),
        migrations.RemoveField(
            model_name='account',
            name='paragon_hc_s',
        ),
        migrations.RemoveField(
            model_name='account',
            name='paragon_sc',
        ),
        migrations.RemoveField(
            model_name='account',
            name='paragon_sc_s',
        ),
        migrations.AddField(
            model_name='accounthistory',
            name='account',
            field=models.ForeignKey(to='accounts.Account'),
        ),
    ]
