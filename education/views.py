from django.shortcuts import render
from rest_framework import viewsets, generics, status
from education.models import *
from payments.models import *
from education.serializers import *
from education.permissions import IsOwner, IsModerator
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.template import loader
from education.paginators import LessonsPaginator
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import stripe
from stripe import InvalidRequestError
from django.http import request


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonsPaginator
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve', 'update']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk: int):
        course = get_object_or_404(Course, pk=pk)
        Subscription.objects.create(course=course, user=request.user)
        return Response(status=201)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk: int):
        course = get_object_or_404(Course, pk=pk)
        Subscription.objects.filter(course=course, user=request.user).delete()
        return Response(status=204)



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

