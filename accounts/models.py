from django.db import models
from jsonfield import JSONField


class Account(models.Model):
    """
    Model representing Bnet account data.
    Stores data which history isn't tracked.
    """
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
    """
    Model for storing Bnet account data which daily changes need to be tracked.
    An instance is made once a day when the account is inspected for the first
    time a given day if the player played D3 since the last registered date.
    """
    related_account = models.ForeignKey(Account, related_name='history')
    date = models.DateField(auto_now_add=True)
    paragon_sc = models.IntegerField()
    paragon_hc = models.IntegerField()
    paragon_sc_s = models.IntegerField()
    paragon_hc_s = models.IntegerField()
    monsters = models.IntegerField()
    elites = models.IntegerField()
    monsters_hc = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Accounts History'

    def __str__(self):
        data = {
            'battle_tag': self.related_account.battle_tag,
            'date': self.date.strftime('%Y-%m-%d')
        }
        return "{battle_tag} | {date}".format(**data)
