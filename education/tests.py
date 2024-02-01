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

class CourseSubscriptionsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.course = Course.objects.create(title='title', owner=self.user)
        self.auth_client = deepcopy(self.client)
        self.auth_client.force_authenticate(self.user)
        self.subscribe_url = reverse('education:courses-subscribe', args=[self.course.pk])
        self.unsubscribe_url = reverse('education:courses-unsubscribe', args=[self.course.pk])

    def test_anonymous_user_cannot_subscribe(self):
        response = self.client.post(self.subscribe_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_unsubscribe(self):
        url = reverse('education:courses-unsubscribe', args=[self.course.pk])
        response = self.client.post(self.unsubscribe_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_can_subscribe_on_course(self):
        response = self.auth_client.post(self.subscribe_url)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(self.course.subscriptions.get().user, self.user)

    def test_authenticated_client_cant_subscribe_on_not_existing_course(self):
        not_existing_course_id = self.course.pk + 1
        url = reverse('education:courses-subscribe', args=[not_existing_course_id])

        response = self.auth_client.post(url)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_unsubscribe_on_course(self):
        Subscription.objects.create(course=self.course, user=self.user)

        response = self.auth_client.post(self.unsubscribe_url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(self.course.subscriptions.count(), 0)

    def test_set_flag_if_user_subscribed_on_course_or_not(self):
        url = reverse('education:courses-detail', args=[self.course.pk])

        response = self.auth_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['is_subscribed'])

        Subscription.objects.create(course=self.course, user=self.user)

        response = self.auth_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['is_subscribed'])
