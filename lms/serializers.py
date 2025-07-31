from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_quantity = SerializerMethodField()
    lessons_info = SerializerMethodField()

    def get_lessons_quantity(self, obj):
        return obj.lesson_set.count()

    def get_lessons_info(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
