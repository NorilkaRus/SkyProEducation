# Generated by Django 5.0.1 on 2024-02-03 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_remove_subscription_subscribed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='education.course', verbose_name='курс'),
        ),
    ]
