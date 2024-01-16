from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter
from education.views import CourseViewSet, LessonViewSet

app_name = EducationConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [] + router.urls