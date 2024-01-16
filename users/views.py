from django.shortcuts import render
from rest_framework import generics
from users.serializers import UserSerializer
from users.models import User

# Create your views here.
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
