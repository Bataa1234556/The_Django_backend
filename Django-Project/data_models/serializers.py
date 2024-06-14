# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'areacode', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            areacode=validated_data['areacode'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
