from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_quantity = SerializerMethodField()
    lessons_info = SerializerMethodField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_lessons_quantity(self, obj):
        return obj.lesson_set.count()

    def get_lessons_info(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = "__all__"
