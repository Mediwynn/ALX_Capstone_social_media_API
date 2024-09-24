from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from .models import User, Post, Follower
from .serializers import UserSerializer, PostSerializer, FollowerSerializer
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        following = request.user.following.values_list('following', flat=True)
        posts = Post.objects.filter(user_id__in=following).order_by('-timestamp')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
