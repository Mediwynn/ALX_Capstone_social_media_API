from django.urls import path
from .views import PostCreateView, PostListView, PostDetailView, FeedListView, like_post, CommentCreateView, PostDeleteView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('', PostListView.as_view(), name='list_posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Handles both GET, PUT, DELETE
    path('feed/', FeedListView.as_view(), name='feed'),
    path('like/<int:pk>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
]
