from django.urls import path
from .views import FollowCreateView, FollowDeleteView

urlpatterns = [
    path('follow/<int:following_id>/', FollowCreateView.as_view(), name='follow'),
    path('unfollow/<int:following_id>/', FollowDeleteView.as_view(), name='unfollow'),
]
