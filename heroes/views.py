from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Hero
from .serializers import HeroSerializer


class HeroView(APIView):

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
