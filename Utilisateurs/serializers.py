from rest_framework import serializers
from .models import CustomUser, Message


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nom', 'prenom', 'photo', 'role', 'is_active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'nom', 'prenom', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']
