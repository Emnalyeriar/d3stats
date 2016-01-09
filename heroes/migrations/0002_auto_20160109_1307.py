# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegendaryPower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('info', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Passives',
            new_name='Passive',
        ),
        migrations.RenameModel(
            old_name='Runes',
            new_name='Rune',
        ),
        migrations.RenameModel(
            old_name='Skills',
            new_name='Skill',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='paragon',
        ),
        migrations.RemoveField(
            model_name='herohistory',
            name='last_played',
        ),
        migrations.AddField(
            model_name='hero',
            name='battle_tag',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hero',
            name='dead',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hero',
            name='hero_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hero',
            name='account',
            field=models.ForeignKey(blank=True, to='accounts.Account'),
        ),
    ]
