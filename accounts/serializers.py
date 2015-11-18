from rest_framework import serializers

from .models import Account, AccountHistory


class AccountHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountHistory
        exclude = ('related_account',)


class BaseAccountSerializer(serializers.ModelSerializer):
    last_history = AccountHistorySerializer(read_only=True)
    rank = Account.objects

    class Meta:
        model = Account
        fields = ('region', 'battle_tag', 'last_updated', 'last_played',
                  'heroes', 'guild_name', 'time_played', 'last_history')


class AccountSerializer(serializers.ModelSerializer):
    history = AccountHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('region', 'battle_tag', 'last_updated', 'last_played',
                  'heroes', 'guild_name', 'time_played', 'history',)
