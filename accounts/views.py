from datetime import datetime

from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions

from battlenet.API import get_account

from .models import Account, AccountHistory
from .serializers import BaseAccountSerializer, AccountSerializer


class AccountView(APIView):
    def get(self, request, region=None, battle_tag=None, format=None):
        if region is None or battle_tag is None:
            accounts = Account.objects.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)

        battle_tag_hash = battle_tag.replace('-', '#')
        account = Account.objects.filter(
            battle_tag__iexact=battle_tag_hash).first()
        account_history = AccountHistory.objects.order_by(
            '-date').filter(account=account)

        if (not account or
           not account_history or
           account.last_updated.date() != timezone.now().date()):

            APIresponse = get_account(region, battle_tag)
            if APIresponse.status_code != 200:
                return Response({
                    'status': 'Internal Server Error',
                    'message': 'Cannot connect to Battle.net'
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = APIresponse.json()
            data['lastUpdated'] = datetime.fromtimestamp(
                int(data['lastUpdated'])).date()

            if 'code' in data and data['code'] == 'NOTFOUND':
                return Response({
                    'status': 'Not Found',
                    'message': 'The account could not be found'
                }, status.HTTP_404_NOT_FOUND)

            if not account:
                account = Account(
                    region=region,
                    battle_tag=data['battleTag'],
                    last_played=data['lastUpdated'],
                    heroes=data['heroes'],
                    guild_name=data['guildName'],
                    time_played=data['timePlayed']
                )
                account.save()

            if (not account_history or
               data['lastUpdated'] > account.last_played):

                account_history_today = AccountHistory(
                    account=account,
                    paragon_sc=data['paragonLevel'],
                    paragon_hc=data['paragonLevelHardcore'],
                    paragon_sc_s=data['paragonLevelSeason'],
                    paragon_hc_s=data['paragonLevelSeasonHardcore'],
                    monsters=data['kills']['monsters'],
                    elites=data['kills']['elites'],
                    monsters_hc=data['kills']['hardcoreMonsters'],
                )
                account_history_today.save()

            if (data['lastUpdated'] > account.last_played):
                account.last_played = data['lastUpdated']
                account.heroes = data['heroes'],
                account.guild_name = data['guildName'],
                account.time_played = data['timePlayed']
                account.save()
            else:
                account.save()

        serializer = AccountSerializer(instance=account)
        return Response(serializer.data)


class RecentlyUpdatedView(APIView):
    def get(self, request, format=None):
        accounts = Account.objects.order_by('-last_updated')[:10]
        serializer = BaseAccountSerializer(accounts, many=True)
        return Response(serializer.data)
