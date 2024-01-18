from django.db import models
from rest_framework import serializers

# Create your models here.
NULLABLE = {'blank':  True, 'null': True}

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)

    def __str__(self):
        if self.description:
            return f'{self.title}: {self.description}'
        else:
            return f'{self.title}: нет описания'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    url = models.CharField(max_length=100, verbose_name='ссылка')
    course = models.ForeignKey(
        'education.Course',
        on_delete=models.CASCADE,
        verbose_name='курс',
    )

    def __str__(self):
        if self.description:
            return f'{self.title} ({self.url}): {self.description}'
        else:
            return f'{self.title} ({self.url}): нет описания'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

