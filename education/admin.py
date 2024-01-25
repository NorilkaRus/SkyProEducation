from django.contrib import admin
from education import models
# Register your models here.

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'preview', 'owner',)
    list_filter = ('title', 'owner',)
    search_fields = ('title', 'description', 'owner',)


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'preview', 'url', 'course', 'owner',)
    list_filter = ('title', 'course', 'owner',)
    search_fields = ('title', 'description', 'url', 'course', 'owner',)