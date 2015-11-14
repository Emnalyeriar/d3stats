from datetime import datetime
# from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from battlenet.API import get_account

from .models import Account, AccountHistory
from .serializers import AccountSerializer


class AccountView(APIView):
    def get(self, request, region=None, battle_tag=None, format=None):
        if region is None or battle_tag is None:
            accounts = Account.objects.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)
        else:
            battle_tag_hash = battle_tag.replace('-', '#')
            account = Account.objects.filter(
                battle_tag__iexact=battle_tag_hash).first()
            if not account:
                APIresponse = get_account(region, battle_tag)

                if APIresponse.status_code != 200:
                    return Response({
                        'status': 'Internal Server Error',
                        'message': 'Cannot connect to Battle.net'
                    }, status.HTTP_500_INTERNAL_SERVER_ERROR)

                data = APIresponse.json()

                if 'code' in data and data['code'] == 'NOTFOUND':
                    return Response({
                        'status': 'Not Found',
                        'message': 'The account could not be found'
                    }, status.HTTP_404_NOT_FOUND)

                account = Account(
                    battle_tag=data['battleTag'],
                    last_played=datetime.fromtimestamp(
                        int(data['lastUpdated'])).date(),
                    heroes=data['heroes'],
                    guild_name=data['guildName'],
                    time_played=data['timePlayed']
                )
                account.save()

            serializer = AccountSerializer(account)

            return Response(serializer.data)
