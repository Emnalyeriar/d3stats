from datetime import datetime

import requests

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def get_account(region, battle_tag):
    url_data = (region, battle_tag, settings.BNET_APIKEY,)
    r = requests.get("https://{0}.api.battle.net/"
                     "d3/profile/{1}/?"
                     "locale=en_GB&apikey={2}".format(*url_data))
    if r.status_code != 200:
        return Response({
            'status': 'Internal Server Error',
            'message': 'Cannot connect to Battle.net'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR)
    data = r.json()
    if 'code' in data and data['code'] == 'NOTFOUND':
        return Response({
            'status': 'Not Found',
            'message': 'The account could not be found'
        }, status.HTTP_404_NOT_FOUND)
    data['lastUpdated'] = datetime.fromtimestamp(
        int(data['lastUpdated'])).date()
    return {'data': data}
