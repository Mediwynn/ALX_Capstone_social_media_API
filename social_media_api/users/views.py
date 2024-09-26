from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    #permission_classes = [IsAuthenticated]  # This will now require JWT auth to access

User = get_user_model()

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # You can add logic to prevent certain users from deleting themselves
        if instance == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")
        instance.delete()
