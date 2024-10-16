from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, Comment
from followers.models import Follow
from posts.serializers import PostSerializer, CommentSerializer
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']  # filter posts by the author's ID
    search_fields = ['content']  # search posts by the content

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Check if the user is the author of the post
        if self.get_object().author != self.request.user:
            raise PermissionDenied('You cannot edit this post')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        # Check if the user is the author of the post
        if instance.author != self.request.user:
            raise PermissionDenied('You cannot delete this post')
        instance.delete()

class CustomFeedPagination(PageNumberPagination):
    page_size = 10  # Set the number of posts per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomFeedPagination  # Enable pagination for this view

    def get_queryset(self):
        following = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        queryset = Post.objects.filter(Q(author__in=following) | Q(author=self.request.user))

        # Sorting logic: Default is by 'created_at' but can be overridden by 'sort' query param
        sort_by = self.request.query_params.get('sort', 'created_at')

        if sort_by == 'popularity':
            return queryset.order_by('-likes_count', '-comments_count')  # Sort by likes, then comments
        elif sort_by == 'created_at':
            return queryset.order_by('-created_at')  # Default sort by most recent
        else:
            return queryset.order_by('-created_at')  # Fallback in case of an invalid parameter

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the post object based on the post_id passed in the URL
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        # Save the comment, linking the post and the current user
        serializer.save(post=post, user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Use the default validation and save process
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"detail": "Comment added successfully."}, status=status.HTTP_201_CREATED)
    

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # Ensure that the user is the author before deleting the post
        if instance.author != self.request.user:
            raise PermissionDenied("You cannot delete this post.")
        instance.delete()

@api_view(['POST'])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.likes_count += 1
        post.save()
        return Response({'likes_count': post.likes_count}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
