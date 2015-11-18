from django.db import models
from jsonfield import JSONField


class Account(models.Model):
    REGION_CHOICES = (
        ('eu', 'Europe'),
        ('us', 'Americas'),
        ('kr', 'Korea'),
        ('tw', 'Taiwan'),
    )
    region = models.CharField(choices=REGION_CHOICES, max_length=2)
    battle_tag = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    last_played = models.DateField()
    heroes = JSONField()
    guild_name = models.CharField(max_length=200)
    time_played = JSONField()
    last_history = models.ForeignKey('AccountHistory', blank=True, null=True)

    def __str__(self):
        return self.battle_tag


class AccountHistory(models.Model):
    related_account = models.ForeignKey(Account, related_name='history')
    date = models.DateField(auto_now_add=True)
    paragon_sc = models.IntegerField()
    paragon_hc = models.IntegerField()
    paragon_sc_s = models.IntegerField()
    paragon_hc_s = models.IntegerField()
    monsters = models.IntegerField()
    elites = models.IntegerField()
    monsters_hc = models.IntegerField()

    def __str__(self):
        return self.date
