# users/urls.py
from django.urls import path
from .views import UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update_user'),  # URL for updating user profile
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
]
