from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payment, User
from users.serializers import (
    CustomTokenPairSerializer,
    PaymentSerializer,
    UserSerializer,
)
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "type",
    )
    ordering_fields = ("payment_date",)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Создаем сессию для оплаты курса"""
        payment = serializer.save(user=self.request.client)
        course = payment.course
        amount = payment.payment_amount

        product = create_stripe_product(course)

        price = create_stripe_price(amount, product)

        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.product = product["name"]
        payment.save()


class CustomTokenPairView(TokenObtainPairView):
    """Расширение класса TokenObtainPairView"""

    serializer_class = CustomTokenPairSerializer
