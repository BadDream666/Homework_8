from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.paginators import LessonPaginator, CoursePaginator
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModer,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner | IsModer,)  # Модераторы могут удалять
        else:  # list
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """Подписаться на курс"""
        course = self.get_object()
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course
        )
        if created:
            return Response({'status': 'subscribed'}, status=201)
        return Response({'status': 'already subscribed'}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        """Отписаться от курса"""
        course = self.get_object()
        deleted_count, _ = Subscription.objects.filter(
            user=request.user,
            course=course
        ).delete()
        if deleted_count > 0:
            return Response({'status': 'unsubscribed'})
        return Response({'status': 'not subscribed'}, status=400)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        """Модераторы видят все, обычные пользователи - только свои уроки"""
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]  # Модераторы могут удалять
