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
        elif self.action in ["list", "update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
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
        course = self.get_object()
        deleted = Subscription.objects.filter(
            user=request.user,
            course=course
        ).delete()
        if deleted[0] > 0:
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
    permission_classes = [IsAuthenticated, IsModer | IsOwner]
    pagination_class = LessonPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name="moders").exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset


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
    permission_classes = [IsAuthenticated, IsOwner]
