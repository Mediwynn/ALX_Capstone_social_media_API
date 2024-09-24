from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from .serializers import FollowSerializer
from users.models import User

class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the current user as the follower
        serializer.save(follower=self.request.user)

class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user being unfollowed
        following = User.objects.get(id=self.kwargs['following_id'])
        # Return the follow relationship to delete it
        return Follow.objects.get(follower=self.request.user, following=following)
