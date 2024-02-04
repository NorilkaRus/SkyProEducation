from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

# Create your models here.
NULLABLE = {'blank':  True, 'null': True}

class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)
    sity = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    is_active = models.BooleanField(verbose_name='Активность', default=True)
    last_login = models.DateField(verbose_name='Последний вход', default='2024-02-02', )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

