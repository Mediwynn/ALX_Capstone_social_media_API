from rest_framework import serializers
from .models import Follow
from users.models import User

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']
        read_only_fields = ['follower']

    def validate_following(self, value):
        # Ensure that users can't follow themselves
        if self.context['request'].user == value:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value
