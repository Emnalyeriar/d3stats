from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'udapted_at')

        def create(self, validated_data):
            return User.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get(
                'username', instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
