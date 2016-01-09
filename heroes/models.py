from django.db import models
from jsonfield import JSONField
from accounts.models import Account


class Hero(models.Model):
    """
    Model representing d3 heroes data.
    Stores data which history isn't tracked.
    """
    CLASSES = (
        ('witch-doctor', 'Witch Doctor'),
        ('wizard', 'Wizard'),
        ('crusader', 'Crusader'),
        ('barbarian', 'Barbarian'),
        ('monk', 'Monk'),
        ('demon-hunter', 'Demon Hunter'),
    )
    GENDERS = (
        (1, 'Female'),
        (2, 'Male')
    )
    hero_id = models.IntegerField()
    name = models.CharField(max_length=13)
    account = models.ForeignKey(Account, blank=True)
    battle_tag = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    last_played = models.DateField()
    class_name = models.CharField(choices=CLASSES, max_length=100)
    gender = models.IntegerField(choices=GENDERS)
    # skills = models.ManyToManyField('Skill')
    elites = models.IntegerField()
    # paragon = models.IntegerField()
    hardcore = models.BooleanField()
    seasonal = models.BooleanField()
    dead = models.BooleanField()
    season_created = models.IntegerField()
    last_history = models.ForeignKey('HeroHistory', blank=True, null=True)
    skills = models.ManyToManyField('Skill')
    runes = models.ManyToManyField('Rune')
    passives = models.ManyToManyField('Passive')
    legendary_powers = models.ManyToManyField('LegendaryPower')
    items = JSONField()

    def __str__(self):
        return self.name


class HeroHistory(models.Model):
    """
    Model for storing d3 heroes data which daily changes need to be tracked.
    An instance is made once a day when the account is inspected for the first
    time a given day if the player played D3 since the last registered date.
    """
    related_hero = models.ForeignKey(Hero, related_name='history')
    date = models.DateField(auto_now_add=True)
    life = models.IntegerField()
    damage = models.IntegerField()
    toughness = models.IntegerField()
    healing = models.IntegerField()
    attack_speed = models.IntegerField()
    armor = models.IntegerField()
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    vitality = models.IntegerField()
    intelligence = models.IntegerField()
    physical_resist = models.IntegerField()
    fire_resist = models.IntegerField()
    cold_resist = models.IntegerField()
    lightning_resist = models.IntegerField()
    poison_resist = models.IntegerField()
    arcane_resist = models.IntegerField()
    critDamage = models.IntegerField()
    blockChance = models.IntegerField()
    block_amount_min = models.IntegerField()
    block_amount_max = models.IntegerField()
    damage_increase = models.IntegerField()
    crit_chance = models.IntegerField()
    damage_reduction = models.IntegerField()
    thorns = models.IntegerField()
    life_steal = models.IntegerField()
    life_per_kill = models.IntegerField()
    gold_find = models.IntegerField()
    magic_find = models.IntegerField()
    life_on_hit = models.IntegerField()
    primary_resource = models.IntegerField()
    secondary_resource = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Accounts History'

    def __str__(self):
        data = {
            'battle_tag': self.related_hero.account.battle_tag,
            'name': self.related_hero.name,
            'date': self.date.strftime('%Y-%m-%d')
        }
        return "{battle_tag} | {name} | {date}".format(**data)


class Skill(models.Model):
    """
    Model storing skills that are used by heroes.
    """
    slug = models.CharField(max_length=300)
    info = JSONField()


class Rune(models.Model):
    """
    Model storing runes that are attached to skills.
    """
    slug = models.CharField(max_length=300)
    type = models.CharField(max_length=300)
    info = JSONField()


class Passive(models.Model):
    """
    Model storing passive skills that are used by heroes.
    """
    slug = models.CharField(max_length=300)
    info = JSONField()


class LegendaryPower(models.Model):
    """
    Model storing legendary powers that are used by heroes.
    """
    name = models.CharField(max_length=300)
    info = JSONField()
