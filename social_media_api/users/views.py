# users/views.py
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure the user can only update their own profile
        user = super().get_object()
        if user != self.request.user:
            raise PermissionDenied("You can only update your own profile.")
        return user

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")
        instance.delete()
