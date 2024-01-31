from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from education.models import *
from users.models import *
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your tests here.
#
class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.lesson = Lesson.objects.create(
            title='test_title',
            description='test_description',
            url='youtube.com/123',
            course_id=1
        )
        self.course = Course.objects.create(
            title='test',
        )

    def test_get_list(self):
        """ Тестирование просмотра уроков """
        response = self.client.get(
            reverse('education:lessons-list')
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_create(self):
        """ Тест создания урока """

        data = {
            'title': 'test2',
            'description': self.lesson.description
        }

        response = self.client.post(
            reverse('education:lesson-create'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEquals(
            Lesson.objects.all().count(),
            1
        )

    def test_lesson_create_validation_error(self):
        """ Тест ошибки валидации """
        self.user = User.objects.create(
            email='admin@admin.com',
            first_name='Frida',
            last_name='Shishka',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('admin')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'test3',
            'description': self.lesson.description,
            'video': 'Посторонний ресурс'
        }
        response = self.client.post(
            reverse('education:lesson-create'),
            data=data,
            user=self.user
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_lesson_update(self):
        self.user = User.objects.create(
            email='admin@admin.com',
            first_name='Frida',
            last_name='Shishka',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('admin')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(reverse("education:lesson-subscribe", args=[self.lesson.pk]), data={
            'title': 'test_title1',
            'description': 'Test Description Update',
            'url': 'youtube.com/1234',
            'course_id': 1
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json(),
            {'description': 'Test Description Update', 'course': 1, 'title': 'test_title1', 'url': 'youtube.com/1234',
             'owner': None, 'preview': None, 'id': 8}
        )

    def test_lesson_delete(self):
        """ Тест удаления урока без авторизации"""
        response = self.client.delete(reverse('education:lesson-subscribe', args=[self.lesson.pk]))
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def tearDown(self):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

class CreateSubscription(APITestCase):

    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='test123',
            description='test123',
        )

        self.lesson = Lesson.objects.create(
            title='test1',
            description='test1',
            url='https://youtube.com',
            course=self.course
        )

        self.user = User.objects.create(
            email='admin@admin.com',
            first_name='Frida',
            last_name='Shishka',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('admin')
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

    def test_create_subscription(self):
        """ Тест создания подписки """
        data = {
            'user': self.user.pk,
            'course': self.course.pk
        }

        response = self.client.post('education:lesson-subscribe', data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_list(self):
        """ Тест просмотра подписок """
        response = self.client.get('education:subscription')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_subscription(self):
        """ Тест удаления подписки """
        response = self.client.delete('education:subscription')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        User.objects.all().delete()
        Course.objects.all().delete()
