from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'email', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'status']

    def update(self, instance, validated_data):
        instance.status = validated_data['get_status_display']
        instance.save()
        return instance
