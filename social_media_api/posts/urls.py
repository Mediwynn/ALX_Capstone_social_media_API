from django.urls import path
from .views import PostCreateView, PostListView, PostDetailView, FeedListView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('', PostListView.as_view(), name='list_posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('feed/', FeedListView.as_view(), name='feed'),
]
