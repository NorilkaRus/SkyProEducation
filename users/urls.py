from users.apps import UsersConfig
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
]
