from django.urls import path
from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter
from education.views import *

app_name = EducationConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
                  path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lessons/<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='lesson-delete'),
                  path('lessons/list/', LessonListAPIView.as_view(), name='lessons-list'),
              ] + router.urls
