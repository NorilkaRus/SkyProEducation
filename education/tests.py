from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from education.models import *
from users.models import *
# Create your tests here.

class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.lesson = Lesson.objects.create(
            title='test_title',
            description = 'test_description'
        )
        self.course = Course.objects.create(
            title='test',
        )


    def test_get_list(self):
        """
        Тестирование просмотра уроков
        """

        response = self.client.get(
            reverse('education:lesson_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )


    def test_lesson_create(self):
        """
        Тест создания урока
        """

        data = {
            'title': 'test2',
            'description': self.lesson.description
        }

        response = self.client.post(
            reverse('education:lesson_create'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_create_validation_error(self):
        """
        Тест ошибки валидации
        """

        data = {
            'title': 'test3',
            'description': self.lesson.description,
            'video': 'Посторонний ресурс'
        }

        response = self.client.post(
            reverse('education:lesson_create'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_lesson_update(self):
        response = self.client.patch(reverse("education:lesson_update", args=[self.lesson.pk]), data={
            'title': self.lesson.pk,
            'description': 'Test Description Update',
        })

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {'description': 'Test Description Update', 'id': 1, 'title': 'test', 'url': None }

        )



    def test_lesson_delete(self):
        """ Тест удаления урока без авторизации"""

        response = self.client.delete(reverse('education:lesson_delete', args=[self.lesson.pk]))

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
        self.user = User.objects.create(
            email='admin1@admin.com',
            is_staff=True,
            is_active=True,
        )
        self.user.set_password('admin1')
        self.user.save()
        self.client.force_authenticate(self.user)

        self.course = Course.objects.create(
            title='test'
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            subscribed=True
        )

    def test_sub_create(self):
        """
        Тест создания подписки
        """

        data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'subscribed': False
        }

        response = self.client.post(
            reverse('education:subscription_create'),
            data=data
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


    def test_sub_update(self):
        """
        Тестирование обновления подписки
        """

        data = {
            'user': self.subscription.user.pk,
            'course':self.subscription.course.pk,
            'subscribed': True
        }

        response = self.client.put(
            reverse('education:subscription_update', args=[self.subscription.pk]), data=data)


        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {'id': 4, 'subscribed': True, 'user': 3, 'course': 3}

        )


    def test_sub_delete(self):

        response = self.client.delete(reverse('education:subscription_delete', kwargs={'pk': self.subscription.pk}))

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Subscription.objects.all().delete()