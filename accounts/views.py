from datetime import datetime

from django.utils import timezone

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from battlenet.API import get_account

from .models import Account, AccountHistory
from .serializers import BaseAccountSerializer, AccountSerializer
from .paginations import LeaderboardsPagination


class AccountView(APIView):
    """
    Main View for Account model.

    This view checks if Account was already inspected today. If so it just
    return the account data from db, otherwise makes a new Account instance
    or updated the data based on Battle.net API data.

    @get /api/accounts -> displays all accounts adata #just for debugging
    @get /api/accounts/<region>/<battle_tag>/ -> displays bnet account data
    """
    def get(self, request, region=None, battle_tag=None, format=None):
        if region is None or battle_tag is None:
            if request.user.is_staff:
                accounts = Account.objects.all()
                serializer = AccountSerializer(accounts, many=True)
                return Response(serializer.data)
            else:
                return Response({
                    'status': 'Forbidden',
                    'message': 'Admin only view'
                }, status=status.HTTP_403_FORBIDDEN)

        account = Account.objects.filter(
            battle_tag__iexact=battle_tag, region=region).first()
        account_history = AccountHistory.objects.order_by(
            '-date').filter(account=account)

        if (not account or
           not account_history or
           account.last_updated.date() != timezone.now().date()):
            APIresponse = get_account(region, battle_tag)
            if isinstance(APIresponse, Response):
                return APIresponse
            data = APIresponse['data']

            if not account:
                account = Account(
                    region=region,
                    battle_tag=data['battleTag'].replace('#', '-'),
                    last_played=data['lastUpdated'],
                    heroes=data['heroes'],
                    guild_name=data['guildName'],
                    time_played=data['timePlayed']
                )
                account.save()

            if (not account_history or
               data['lastUpdated'] > account.last_played):

                account_history_today = AccountHistory(
                    related_account=account,
                    paragon_sc=data['paragonLevel'],
                    paragon_hc=data['paragonLevelHardcore'],
                    paragon_sc_s=data['paragonLevelSeason'],
                    paragon_hc_s=data['paragonLevelSeasonHardcore'],
                    monsters=data['kills']['monsters'],
                    elites=data['kills']['elites'],
                    monsters_hc=data['kills']['hardcoreMonsters'],
                )
                account_history_today.save()
                account.last_history = account_history_today

            if (data['lastUpdated'] > account.last_played):
                account.last_played = data['lastUpdated']
                account.heroes = data['heroes'],
                account.guild_name = data['guildName'],
                account.time_played = data['timePlayed']

            account.save()

        serializer = AccountSerializer(account)
        return Response(serializer.data)


class RecentlyUpdatedView(APIView):
    """
    Shows the last 10 updated accounts.
    """
    def get(self, request, format=None):
        accounts = Account.objects.order_by('-last_updated')[:10]
        serializer = BaseAccountSerializer(accounts, many=True)
        return Response(serializer.data)


class LeaderboardsView(generics.ListAPIView):
    """
    Shows accounts leaderboards.

    @get /api/accounts/leaderboards/<region>/<league>/ -> shows leaders boards
    for specified region and league
    """
    serializer_class = BaseAccountSerializer
    model = Account
    pagination_class = LeaderboardsPagination

    def get_queryset(self):
        region = self.kwargs['region']
        query = '-last_history__paragon_'
        query += self.kwargs['league'].replace('-', '_')
        if region == 'all':
            accounts = Account.objects.all()
        else:
            accounts = Account.objects.filter(region=region)
        queryset = accounts.order_by(query)
        return queryset
