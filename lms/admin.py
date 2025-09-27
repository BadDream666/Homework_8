from django.contrib import admin
from lms.models import Course, Lesson, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'subscribed_at']
    list_filter = ['subscribed_at', 'course']
    search_fields = ['user__email', 'course__name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'lessons_count']
    list_filter = ['owner']
    search_fields = ['name', 'description']

    def lessons_count(self, obj):
        return obj.lesson_set.count()

    lessons_count.short_description = 'Количество уроков'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'owner']
    list_filter = ['course', 'owner']
    search_fields = ['name', 'description']
