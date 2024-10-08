from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Make password write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}
        ref_name = 'UserProfileSerializer'  # Add a unique ref_name here

    def create(self, validated_data):
        # Create user using create_user to ensure password is hashed
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data.get('bio', ''),  # Use get to provide a default value
            profile_picture=validated_data.get('profile_picture', None)  # Handle optional fields
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()  # Save the user instance to the database
        return user
