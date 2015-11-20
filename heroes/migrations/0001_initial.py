# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20151120_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=13)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('last_played', models.DateField()),
                ('class_name', models.CharField(choices=[('witch-doctor', 'Witch Doctor'), ('wizard', 'Wizard'), ('crusader', 'Crusader'), ('barbarian', 'Barbarian'), ('monk', 'Monk'), ('demon-hunter', 'Demon Hunter')], max_length=100)),
                ('gender', models.IntegerField(choices=[(1, 'Female'), (2, 'Male')])),
                ('elites', models.IntegerField()),
                ('paragon', models.IntegerField()),
                ('hardcore', models.BooleanField()),
                ('seasonal', models.BooleanField()),
                ('season_created', models.IntegerField()),
                ('legendary_powers', jsonfield.fields.JSONField()),
                ('items', jsonfield.fields.JSONField()),
                ('account', models.ForeignKey(to='accounts.Account')),
            ],
        ),
        migrations.CreateModel(
            name='HeroHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('last_played', models.DateField()),
                ('life', models.IntegerField()),
                ('damage', models.IntegerField()),
                ('toughness', models.IntegerField()),
                ('healing', models.IntegerField()),
                ('attack_speed', models.IntegerField()),
                ('armor', models.IntegerField()),
                ('strength', models.IntegerField()),
                ('dexterity', models.IntegerField()),
                ('vitality', models.IntegerField()),
                ('intelligence', models.IntegerField()),
                ('physical_resist', models.IntegerField()),
                ('fire_resist', models.IntegerField()),
                ('cold_resist', models.IntegerField()),
                ('lightning_resist', models.IntegerField()),
                ('poison_resist', models.IntegerField()),
                ('arcane_resist', models.IntegerField()),
                ('critDamage', models.IntegerField()),
                ('blockChance', models.IntegerField()),
                ('block_amount_min', models.IntegerField()),
                ('block_amount_max', models.IntegerField()),
                ('damage_increase', models.IntegerField()),
                ('crit_chance', models.IntegerField()),
                ('damage_reduction', models.IntegerField()),
                ('thorns', models.IntegerField()),
                ('life_steal', models.IntegerField()),
                ('life_per_kill', models.IntegerField()),
                ('gold_find', models.IntegerField()),
                ('magic_find', models.IntegerField()),
                ('life_on_hit', models.IntegerField()),
                ('primary_resource', models.IntegerField()),
                ('secondary_resource', models.IntegerField()),
                ('related_hero', models.ForeignKey(to='heroes.Hero', related_name='history')),
            ],
            options={
                'verbose_name_plural': 'Accounts History',
            },
        ),
        migrations.CreateModel(
            name='Passives',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=300)),
                ('info', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Runes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=300)),
                ('type', models.CharField(max_length=300)),
                ('info', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=300)),
                ('info', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.AddField(
            model_name='hero',
            name='last_history',
            field=models.ForeignKey(blank=True, null=True, to='heroes.HeroHistory'),
        ),
        migrations.AddField(
            model_name='hero',
            name='passives',
            field=models.ManyToManyField(to='heroes.Passives'),
        ),
        migrations.AddField(
            model_name='hero',
            name='runes',
            field=models.ManyToManyField(to='heroes.Runes'),
        ),
        migrations.AddField(
            model_name='hero',
            name='skills',
            field=models.ManyToManyField(to='heroes.Skills'),
        ),
    ]
