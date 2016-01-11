import datetime

from django.utils import timezone
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from battlenet.API import BnetAPI

from accounts.models import Account
from .models import Hero, HeroHistory, Skill, Rune, Passive, LegendaryPower
from .serializers import HeroSerializer, BaseHeroSerializer
from .paginations import LeaderboardsPagination


class HeroView(APIView):
    """
    Main View for Hero model.

    This view checks if Hero was already inspected today. If so it just
    returns the hero data from db, otherwise it makes a new Hero instance
    or updates the data based on Battle.net API data.

    @get /api/heroes -> displays all heroes adata #just for debugging
    @get /api/heroes/<region>/<battle_tag>/<hero_id> -> displays bnet hero data
    """
    def get(self, request, region=None, battle_tag=None, hero_id=None):

        if region is None or battle_tag is None or hero_id is None:
            if request.user.is_staff:
                heroes = Hero.objects.all()
                serializer = HeroSerializer(heroes, many=True)
                return Response(serializer.data)
            else:
                return Response({
                    'status': 'Forbidden',
                    'message': 'Admin only view'
                }, status=status.HTTP_403_FORBIDDEN)

        account = Account.objects.filter(
            battle_tag__iexact=battle_tag, region=region).first()
        if not account:
            return Response({
                'status': 'No account data',
                'message': 'Get account data first'
            }, status.HTTP_200_OK)

        hero = Hero.objects.filter(
            hero_id=hero_id, account=account).first()
        hero_history = HeroHistory.objects.order_by(
            '-date').filter(related_hero=hero)

        if (not hero or not hero_history or
           hero.last_updated.date() != timezone.now().date()):
            API = BnetAPI(region, battle_tag, hero_id)
            if API.is_valid():
                data = API.data
            else:
                return API.response

            if not hero:
                # last_played = datetime.date.fromtimestamp(data['last-updated'])
                last_played = data['last-updated']
                hero = Hero(
                    hero_id=data['id'],
                    name=data['name'],
                    account=account,
                    battle_tag=battle_tag,
                    last_played=last_played,
                    class_name=data['class'],
                    gender=data['gender'],
                    elites=data['kills']['elites'],
                    hardcore=data['hardcore'],
                    seasonal=data['seasonal'],
                    dead=data['dead'],
                    season_created=data['seasonCreated'],
                    items=data['items'],
                )
                hero.save()
                update_skills(hero, data)

            if (not hero_history or
               data['lastUpdated'] > hero.last_played):

                hero_history_today = HeroHistory(
                    related_hero=hero,
                    life=data['stats']['life'],
                    damage=data['stats']['damage'],
                    toughness=data['stats']['toughness'],
                    healing=data['stats']['healing'],
                    attack_speed=data['stats']['attackSpeed'],
                    armor=data['stats']['armor'],
                    strength=data['stats']['strength'],
                    dexterity=data['stats']['dexterity'],
                    vitality=data['stats']['vitality'],
                    intelligence=data['stats']['intelligence'],
                    physical_resist=data['stats']['physicalResist'],
                    fire_resist=data['stats']['fireResist'],
                    cold_resist=data['stats']['coldResist'],
                    lightning_resist=data['stats']['lightningResist'],
                    poison_resist=data['stats']['poisonResist'],
                    arcane_resist=data['stats']['arcaneResist'],
                    crit_damage=data['stats']['critDamage'],
                    blockChance=data['stats']['blockChance'],
                    block_amount_min=data['stats']['blockAmountMin'],
                    block_amount_max=data['stats']['blockAmountMax'],
                    damage_increase=data['stats']['damageIncrease'],
                    crit_chance=data['stats']['critChance'],
                    damage_reduction=data['stats']['damageReduction'],
                    thorns=data['stats']['thorns'],
                    life_steal=data['stats']['lifeSteal'],
                    life_per_kill=data['stats']['lifePerKill'],
                    gold_find=data['stats']['goldFind'],
                    magic_find=data['stats']['magicFind'],
                    life_on_hit=data['stats']['lifeOnHit'],
                    primary_resource=data['stats']['primaryResource'],
                    secondary_resource=data['stats']['secondaryResource'],
                )
                hero_history_today.save()
                hero.last_history = hero_history_today

            if data['last-updated'] > hero.last_played:
                hero.last_played = data['last-updated']
                hero.elites = data['kills']['elites']
                hero.dead = data['dead']
                hero.items = data['items']
                update_skills(hero, data)
            hero.save()
        serializer = HeroSerializer(hero)
        return Response(serializer.data)


def update_skills(hero, data):
    hero.skills.clear()
    hero.runes.clear()
    for skill in data['skills']['active']:
        current_skill = skill['skill']
        current_rune = skill['rune']
        db_skill = Skill.objects.filter(slug=current_skill['slug']).first()
        if not db_skill:
            db_skill = Skill(
                slug=current_skill['slug'],
                info=current_skill
            )
            db_skill.save()
        hero.skills.add(db_skill)
        db_rune = Rune.objects.filter(slug=current_rune['slug']).first()
        if not db_rune:
            db_rune = Rune(
                slug=current_rune['slug'],
                type=current_rune['type'],
                info=current_rune
            )
            db_rune.save()
        hero.runes.add(db_rune)
    hero.passives.clear()
    for passive in data['skills']['passive']:
        current_passive = passive['skill']
        db_passive = Passive.objects.filter(
            slug=current_passive['slug']
        ).first()
        if not db_passive:
            db_passive = Passive(
                slug=current_passive['slug'],
                info=current_passive
            )
            db_passive.save()
        hero.passives.add(db_passive)
    hero.legendary_powers.clear()
    for power in data['legendaryPowers']:
        if power is None:
            continue
        db_power = LegendaryPower.objects.filter(
            name=power['name']
        ).first()
        if not db_power:
            db_power = LegendaryPower(
                name=power['name'],
                info=power
            )
            db_power.save()
        hero.legendary_powers.add(db_power)


class HeroRecentlyUpdatedView(APIView):
    """
    Shows the last 10 updated heroes.
    """
    def get(self, request, format=None):
        heroes = Hero.objects.order_by('-last_updated')[:10]
        serializer = BaseHeroSerializer(heroes, many=True)
        return Response(serializer.data)


class HeroLeaderboardsView(generics.ListAPIView):
    """
    Shows heroes leaderboards.

    @get /api/heroes/leaderboards/<region>/<league>/<stat>/
    -> shows leaderoards for specified region, league and stat
    """
    serializer_class = BaseHeroSerializer
    model = Hero
    pagination_class = LeaderboardsPagination

    def get_queryset(self):
        region = self.kwargs['region']
        stat = self.kwargs['stat'].replace('-', '_')
        query = '-last_history__'+stat
        league = self.kwargs['league']
        if region == 'all':
            heroes = Hero.objects.all()
        else:
            heroes = Hero.objects.filter(account__region=region)
        if league == 'sc':
            hardcore = False
            seasonal = False
        elif league == 'hc':
            hardcore = True
            seasonal = False
        elif league == 'sc-s':
            hardcore = False
            seasonal = True
        elif league == 'hc-s':
            hardcore = True
            seasonal = True
        heroes = heroes.filter(hardcore=hardcore, seasonal=seasonal)
        queryset = heroes.order_by(query)
        return queryset
