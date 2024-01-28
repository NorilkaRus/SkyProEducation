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
    subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_subscribed(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            print(request and request.user)
            return Subscription.objects.filter(user=request.user, course=instance, subscribed=True).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
