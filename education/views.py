from django.shortcuts import render
from rest_framework import viewsets, generics
from education.models import *
from education.serializers import *
from education.permissions import IsOwner, IsModerator
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template import loader
from education.paginators import LessonsPaginator


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonsPaginator
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]



class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonDetailAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDeleteAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]
    pagination_class = LessonsPaginator

def index(request):
    template = loader.get_template('education/index.html')
    objects = Course.objects.all()
    context = {'objects': objects}
    return HttpResponse(template.render(context, request))


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionUpdateView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwner]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner]
