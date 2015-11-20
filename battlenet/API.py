from datetime import datetime

import requests

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


class BnetAPI:
    def __init__(self, region, battle_tag, hero_id=None):
        self.region = region
        self.battle_tag = battle_tag
        self.hero_id = hero_id
        if self.hero_id is None:
            self.get_account_data()
        else:
            self.get_hero_data()

    def get_account_data(self):
        url_data = (self.region, self.battle_tag, settings.BNET_APIKEY,)
        self.response = requests.get(
            "https://{0}.api.battle.net/"
            "d3/profile/{1}/?"
            "locale=en_GB&apikey={2}".format(*url_data)
        )

    def get_hero_data():
        pass

    def is_valid(self):
        if self.response.status_code != 200:
            self.set_response_to_500()
            return False

        data = self.response.json()
        if 'code' in data and data['code'] == 'NOTFOUND':
            self.set_response_to_404()
            return False

        data['lastUpdated'] = datetime.fromtimestamp(
            int(data['lastUpdated'])).date()
        self.set_data(data)
        return True

    def set_data(self, data):
        self.data = data

    def set_response_to_500(self):
        self.response = Response({
            'status': 'Internal Server Error',
            'message': 'Cannot connect to Battle.net'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_response_to_404(self):
        self.response = Response({
            'status': 'Not Found',
            'message': 'The account could not be found'
        }, status.HTTP_404_NOT_FOUND)
