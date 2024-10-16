# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data.get('bio', ''),  # Use get to provide a default value
            profile_picture=validated_data.get('profile_picture', None)  # Handle optional fields
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Hash the password if it's updated
        instance.save()
        return instance
