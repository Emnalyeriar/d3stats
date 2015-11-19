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
        rank_sc = Account.objects.filter(
            last_history__paragon_sc__gt=instance.last_history.paragon_sc
        ).count()
        region_rank_sc = Account.objects.filter(
            last_history__paragon_sc__gt=instance.last_history.paragon_sc,
            region=instance.region
        ).count()
        rank_hc = Account.objects.filter(
            last_history__paragon_hc__gt=instance.last_history.paragon_hc
        ).count()
        region_rank_hc = Account.objects.filter(
            last_history__paragon_hc__gt=instance.last_history.paragon_hc,
            region=instance.region
        ).count()
        rank_sc_s = Account.objects.filter(
            last_history__paragon_sc_s__gt=instance.last_history.paragon_sc_s
        ).count()
        region_rank_sc_s = Account.objects.filter(
            last_history__paragon_sc_s__gt=instance.last_history.paragon_sc_s,
            region=instance.region
        ).count()
        rank_hc_s = Account.objects.filter(
            last_history__paragon_hc_s__gt=instance.last_history.paragon_hc_s
        ).count()
        region_rank_hc_s = Account.objects.filter(
            last_history__paragon_hc_s__gt=instance.last_history.paragon_hc_s,
            region=instance.region
        ).count()
        data['rank_sc'] = rank_sc + 1
        data['rank_hc'] = rank_hc + 1
        data['rank_sc_s'] = rank_sc_s + 1
        data['rank_hc_s'] = rank_hc_s + 1
        data['region_rank_sc'] = region_rank_sc + 1
        data['region_rank_hc'] = region_rank_hc + 1
        data['region_rank_sc_s'] = region_rank_sc_s + 1
        data['region_rank_hc_s'] = region_rank_hc_s + 1
        return data

    class Meta:
        model = Account
        fields = ('region', 'battle_tag', 'last_updated', 'last_played',
                  'heroes', 'guild_name', 'time_played', 'history',)
