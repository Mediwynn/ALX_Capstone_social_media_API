from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        # Call the original create method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Return a custom message upon successful follow
        return Response({"detail": "Successfully followed."}, status=status.HTTP_201_CREATED)

class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user being unfollowed
        following = get_object_or_404(User, id=self.kwargs['following_id'])
        # Return the follow relationship to delete it
        return get_object_or_404(Follow, follower=self.request.user, following=following)

    def destroy(self, request, *args, **kwargs):
        # Delete the follow relationship
        self.perform_destroy(self.get_object())
        # Return a custom message upon successful unfollow
        return Response({"detail": "Successfully unfollowed."}, status=status.HTTP_200_OK)

class FollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return the follows for the current user
        return Follow.objects.filter(follower=self.request.user)
