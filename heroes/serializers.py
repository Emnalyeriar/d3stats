from rest_framework import serializers

from .models import Hero, HeroHistory


class HeroSerializer(serializers.ModelSerializer):
    """
    Serializer for hero model
    """

    class Meta:
        model = Hero
