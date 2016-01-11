from rest_framework import serializers

from .models import Hero, HeroHistory, Skill, Rune, Passive, LegendaryPower


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for Skill model
    """

    class Meta:
        model = Skill
        fields = ('slug', 'info',)


class PassiveSerializer(serializers.ModelSerializer):
    """
    Serializer for Passive model
    """

    class Meta:
        model = Passive
        fields = ('slug', 'info',)


class RuneSerializer(serializers.ModelSerializer):
    """
    Serializer for Rune model
    """

    class Meta:
        model = Rune
        fields = ('slug', 'type', 'info',)


class LegendaryPowerSerializer(serializers.ModelSerializer):
    """
    Serializer for LegendaryPower model
    """

    class Meta:
        model = LegendaryPower
        fields = ('name', 'info',)


class HeroHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for HeroHistory model
    """

    class Meta:
        model = HeroHistory
        exclude = ('related_hero',)


class BaseHeroSerializer(serializers.ModelSerializer):
    """
    Basic Hero model serializer containing last history registry
    """
    last_history = HeroHistorySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    runes = RuneSerializer(many=True, read_only=True)
    passives = PassiveSerializer(many=True, read_only=True)
    legendary_powers = LegendaryPowerSerializer(many=True, read_only=True)

    class Meta:
        model = Hero
        fields = (
            'hero_id', 'name', 'battle_tag', 'last_updated',
            'last_played', 'class_name', 'gender', 'elites', 'hardcore',
            'seasonal', 'dead', 'season_created', 'skills',
            'runes', 'passives', 'legendary_powers', 'items', 'last_history',
        )


class HeroSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying all data related to a single Hero.
    Contains all hero history and calculates ranks.
    """
    history = HeroHistorySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    runes = RuneSerializer(many=True, read_only=True)
    passives = PassiveSerializer(many=True, read_only=True)
    legendary_powers = LegendaryPowerSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super(HeroSerializer, self).to_representation(instance)
        stats = {
            'rank_damage': 'damage',
            'rank_toughness': 'toughness',
        }
        for rank, stat in stats.items():
            filter = {'last_history__'+stat+'__gt':
                      getattr(instance.last_history, stat),
                      'seasonal': instance.seasonal,
                      'account__region': instance.account.region}
            data[rank] = Hero.objects.filter(**filter).count() + 1
        return data

    class Meta:
        model = Hero
        fields = (
            'hero_id', 'name', 'battle_tag', 'last_updated',
            'last_played', 'class_name', 'gender', 'elites', 'hardcore',
            'seasonal', 'dead', 'season_created', 'skills',
            'runes', 'passives', 'legendary_powers', 'items', 'history',
        )
