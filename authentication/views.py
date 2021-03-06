import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response

from authentication.permissions import IsUserOwner, IsAdmin
from authentication.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    List and create users.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAdmin(),)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': serializer.errors['non_field_errors'][0]
        }, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #
    #         return Response(serializer.validated_data,
    #                         status=status.HTTP_201_CREATED)
    #
    #     return Response({
    #         'status': 'Bad request',
    #         'message': 'Account could not be created with received data'
    #     }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """
    Cookie based login endpoint.
    """
    def post(self, request, format=None):
        data = json.loads(request.body.decode("utf-8"))

        username = data.get('username', None)
        password = data.get('password', None)

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:

                login(request, account)

                serialized = UserSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """
    Logout endpoint.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
