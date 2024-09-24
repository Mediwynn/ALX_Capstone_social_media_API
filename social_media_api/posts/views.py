from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from followers.models import Follow
from posts.serializers import PostSerializer
from django.db.models import Q


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied('You cannot edit this post')
        super().perform_update(serializer)



class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        following = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        queryset = Post.objects.filter(Q(author__in=following) | Q(author=self.request.user))

        # Sorting: default is by 'created_at', but can be overridden by a query parameter
        sort_by = self.request.query_params.get('sort', 'created_at')
        return queryset.order_by(f'-{sort_by}')
