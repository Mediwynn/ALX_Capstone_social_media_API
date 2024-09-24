from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
