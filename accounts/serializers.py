from rest_framework import serializers

from .models import Account, AccountHistory


class AccountHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for AccountHistory model
    """

    class Meta:
        model = AccountHistory
        exclude = ('related_account',)


class BaseAccountSerializer(serializers.ModelSerializer):
    """
    Basic Account model serializer containing last history registry
    """
    last_history = AccountHistorySerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('region', 'battle_tag', 'last_updated', 'last_played',
                  'heroes', 'guild_name', 'time_played', 'last_history')


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying all data related to a single Account.
    Contains all Account history and calculates ranks.
    """
    history = AccountHistorySerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super(AccountSerializer, self).to_representation(instance)
        leagues = {
            'rank_sc': 'paragon_sc',
            'rank_hc': 'paragon_hc',
            'rank_sc_s': 'paragon_sc_s',
            'rank_hc_s': 'paragon_hc_s',
        }
        for rank, paragon in leagues.items():
            filter = {'last_history__'+paragon+'__gt':
                      getattr(instance.last_history, paragon)}
            data[rank] = Account.objects.filter(**filter).count() + 1
        return data

    class Meta:
        model = Account
        fields = ('region', 'battle_tag', 'last_updated', 'last_played',
                  'heroes', 'guild_name', 'time_played', 'history',)
