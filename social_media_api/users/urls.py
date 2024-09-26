from django.urls import path
from .views import UserCreateView, UserDeleteView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
]
