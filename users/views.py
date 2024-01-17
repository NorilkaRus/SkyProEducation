from django.shortcuts import render
from rest_framework import generics
from users.serializers import UserSerializer
from users.models import User

# Create your views here.
class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
