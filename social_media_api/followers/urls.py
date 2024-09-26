from django.urls import path
from .views import FollowCreateView, FollowDeleteView, FollowListView

urlpatterns = [
    path('follow/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/<int:following_id>/', FollowDeleteView.as_view(), name='unfollow'),
    path('', FollowListView.as_view(), name='follow-list'),
]
