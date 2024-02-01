from rest_framework import serializers
from education.models import Course, Lesson, Subscription
from education.validators import YouTubeValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YouTubeValidator(field='url')]


class LessonIncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonIncludeSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        request_user = self.context['request'].user
        if not request_user.is_authenticated:
            return False
        return request_user.subscriptions.filter(course=instance).exists()


    class Meta:
        model = Course
        fields = '__all__'

