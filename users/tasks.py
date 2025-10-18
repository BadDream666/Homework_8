from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_user():
    """Блокирует пользователя, который не заходил больше месяца"""

    today = timezone.now()

    for user in User.objects.all():
        if (today - user.last_login) >= timedelta(weeks=4) and user.is_active:
            user.is_active = False
            user.save()
            print(
                f"пользователь {user.email} был заблокирован из-за отсутствия активности"
            )
