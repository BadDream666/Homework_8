from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import YouTubeValidator


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'subscribed_at']
        read_only_fields = ['user', 'subscribed_at']


class CourseSerializer(ModelSerializer):
    lessons_quantity = SerializerMethodField()
    lessons_info = SerializerMethodField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_subscribed = SerializerMethodField()

    def get_lessons_quantity(self, obj):
        return obj.lesson_set.count()

    def get_lessons_info(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscriptions.filter(user=request.user).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YouTubeValidator(field='video_link')
        ]
