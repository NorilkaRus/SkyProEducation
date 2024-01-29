from django.urls import path
from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter
from education.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )

app_name = EducationConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
                  path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lessons/<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='lesson-delete'),
                  path('lessons/list/', LessonListAPIView.as_view(), name='lessons-list'),

                  path('', index, name='welcome_page'),

                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                  path('courses/<int:pk>/subscribe/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
                  path('courses/<int:pk>/unsubscribe/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),

              ] + router.urls
