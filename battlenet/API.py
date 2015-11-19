import requests

from django.conf import settings


def get_account(region, battle_tag):
    url_data = (region, battle_tag, settings.BNET_APIKEY,)
    r = requests.get("https://{0}.api.battle.net/"
                     "d3/profile/{1}/?"
                     "locale=en_GB&apikey={2}".format(*url_data))
    return r
