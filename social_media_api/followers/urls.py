from django.urls import path
from .views import FollowCreateView, FollowDeleteView, FollowListView, FollowingListView

urlpatterns = [
    path('follow/<int:user_id>/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/<int:following_id>/', FollowDeleteView.as_view(), name='unfollow'),
    path('', FollowListView.as_view(), name='follow-list'),
    path('following/', FollowingListView.as_view(), name='following-list'),  # New endpoint to get following users
]
