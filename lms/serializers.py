from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import LinkValidator


class CourseSerializer(ModelSerializer):
    lessons_quantity = SerializerMethodField()
    lessons_info = SerializerMethodField()
    user_signed = SerializerMethodField(read_only=True)

    def get_lessons_quantity(self, obj):
        return obj.lesson_set.count()

    def get_lessons_info(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def get_user_signed(self, instance):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field="video_link")]


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
