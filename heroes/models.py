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
    name = models.CharField(max_length=13)
    account = models.ForeignKey(Account)
    last_updated = models.DateTimeField(auto_now=True)
    last_played = models.DateField()
    class_name = models.CharField(choices=CLASSES, max_length=100)
    gender = models.IntegerField(choices=GENDERS)
    skills = models.ManyToManyField('Skills')
    elites = models.IntegerField()
    paragon = models.IntegerField()
    hardcore = models.BooleanField()
    seasonal = models.BooleanField()
    season_created = models.IntegerField()
    legendary_powers = JSONField()
    last_history = models.ForeignKey('HeroHistory', blank=True, null=True)
    skills = models.ManyToManyField('Skills')
    runes = models.ManyToManyField('Runes')
    passives = models.ManyToManyField('Passives')
    items = JSONField()
    # skill1 = models.ForeignKey()
    # rune1 = models.ForeignKey()
    # skill2 = models.ForeignKey()
    # rune2 = models.ForeignKey()
    # skill3 = models.ForeignKey()
    # rune3 = models.ForeignKey()
    # skill4 = models.ForeignKey()
    # rune4 = models.ForeignKey()
    # skill5 = models.ForeignKey()
    # rune5 = models.ForeignKey()
    # skill6 = models.ForeignKey()
    # rune6 = models.ForeignKey()
    # passive1 = models.ForeignKey()
    # passive2 = models.ForeignKey()
    # passive3 = models.ForeignKey()
    # passive4 = models.ForeignKey()
    # passive5 = models.ForeignKey()

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
    last_played = models.DateField()
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


class Skills(models.Model):
    """
    Model storing skills that are used by heroes.
    """
    slug = models.CharField(max_length=300)
    info = JSONField()


class Runes(models.Model):
    """
    Model storing runes that are attached to skills.
    """
    slug = models.CharField(max_length=300)
    type = models.CharField(max_length=300)
    info = JSONField()


class Passives(models.Model):
    """
    Model storing passive skills that are used by heroes.
    """
    slug = models.CharField(max_length=300)
    info = JSONField()
