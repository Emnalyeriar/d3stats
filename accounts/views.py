# from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


class AccountView(APIView):
    def get(self, request, format=None):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
