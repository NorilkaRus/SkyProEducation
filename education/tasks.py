from celery import shared_task
from django.core.mail import send_mail

from datetime import timedelta
from django.utils import timezone

from config import settings
from education.models import Course
from users.models import User


@shared_task
def update_course():
    """Рассылка обновления курса"""
    my_mail = ["norilkarus@gmail.com"]
    for item in Lesson.objects.filter(update=True):

        if item.update == True:
            print(f'Обновление курса')
            for i in lesson.course.subscriptions.all():
                send_mail(
                    subject='Курс был обновлен',
                    message='В кусре произошли обновления',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[i.user.email]

                )

            item.update = False
            item.save()


def check_last_login():
    """Проверка последнего входа пользователя"""
    now = timezone.now()
    day_x = now - timedelta(days=30)
    for user in User.objects.all():
        if user.last_login < day_x:
            user.is_active = False
            print("Пользователь теперь неактивен")
            user.save()