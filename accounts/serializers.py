from rest_framework import serializers

from .models import Account, AccountHistory


class AccountHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountHistory
        exclude = ('account',)


class AccountSerializer(serializers.ModelSerializer):
    history = AccountHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('region', 'battle_tag', 'last_updated', 'last_played',
                  'heroes', 'guild_name', 'time_played', 'history')
