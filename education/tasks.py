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
    for item in Course.objects.all():
        if item.description != item.update:
            print(f'Обновление курса')
            send_mail(
                subject='Курс был обновлен',
                message='В кусре произошли обновления',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[my_mail]

            )
            item.description = item.update
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