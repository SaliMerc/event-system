from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','first_name','last_name','role','is_active']

    def create(self, validated_data):
        validated_data.pop('is_active', None)
        user=CustomUser.objects.create_user(**validated_data, is_active=True)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
