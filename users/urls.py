from users.apps import UsersConfig
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserCreateAPIView, UserDetailAPIView, UserUpdateAPIView, UserDeleteAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('user/list/', UserListAPIView.as_view(), name='user-list'),
]
