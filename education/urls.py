from django.urls import path
from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter
from education.views import *

app_name = EducationConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
                  path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='lesson-delete'),
                  path('lesson/list/', LessonListAPIView.as_view(), name='lessons-list'),
              ] + router.urls
