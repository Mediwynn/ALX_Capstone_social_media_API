from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import Follow
from .serializers import FollowSerializer, UserSerializer

class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the user being followed from the URL (via user_id)
        user_to_follow = get_object_or_404(User, id=self.kwargs['user_id'])
        # Set the current user as the follower and the `user_to_follow` as the following
        serializer.save(follower=self.request.user, following=user_to_follow)

    def create(self, request, *args, **kwargs):
        # Pass the request context to the serializer to allow validation
        serializer = self.get_serializer(data=request.data, context={'request': request})
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

class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the users the logged-in user is following
        follows = Follow.objects.filter(follower=self.request.user)
        return [follow.following for follow in follows]

    def list(self, request, *args, **kwargs):
        # Override the default list method to return only the 'following' users
        queryset = self.get_queryset()
        following_users = [follow for follow in queryset]  # Extract 'following' users from the Follow model
        
        # Serialize the list of following users (only the 'following' user data)
        following_serializer = UserSerializer(following_users, many=True)
        return Response(following_serializer.data)
