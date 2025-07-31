from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
urlpatterns += router.urls
