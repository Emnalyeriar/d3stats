from django.db import models
from jsonfield import JSONField


class Account(models.Model):
    battle_tag = models.CharField(max_length=100)
    last_updated = models.DateField(auto_now=True)
    last_played = models.DateField()
    heroes = JSONField()
    paragon_sc = models.IntegerField()
    paragon_hc = models.IntegerField()
    paragon_sc_s = models.IntegerField()
    paragon_hc_s = models.IntegerField()
    guild_name = models.CharField(max_length=200)
    time_played = JSONField()
    # last_hero_played = models.ForeignKey(Hero)
    monsters = models.IntegerField()
    elites = models.IntegerField()
    monsters_hc = models.IntegerField()

    def __str__(self):
        return self.battle_tag
