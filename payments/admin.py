from django.contrib import admin
from payments.models import Payment
# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'course', 'lesson', 'amount', 'payment_method',)
    list_filter = ('user', 'date', 'course', 'lesson', 'amount', 'payment_method',)
    search_fields = ('user', 'date', 'course', 'lesson', 'amount', 'payment_method',)