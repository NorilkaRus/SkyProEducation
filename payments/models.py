from django.db import models
from education.models import Course, Lesson
from users.models import User, NULLABLE

# Create your models here.

class Payment(models.Model):

    PERIODICITY_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    date = models.DateField(verbose_name="дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный урок")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма оплаты")
    payment_method = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, verbose_name="способ оплаты")
    session = models.TextField(**NULLABLE, verbose_name="сессия")
    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')

    def __str__(self):
        return f'{self.user}: {self.amount} ({self.date})'

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"