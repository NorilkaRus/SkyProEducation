from users.apps import UsersConfig
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserUpdateAPIView, UserLogin, UserLogout, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
