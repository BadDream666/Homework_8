from django.conf import settings
from django.db import models


class Subscription(models.Model):
    """
    Модель подписки пользователя на курс
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name='subscriptions'
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата подписки"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.email} - {self.course.name}"


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="Описание курса",
        help_text="Опишите курс",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="lms/previews",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Загрузите превью",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Укажите владельца курса",
        related_name='owned_courses'
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="Описание урока",
        help_text="Опишите урок",
        blank=True,
        null=True,
    )
    picture = models.ImageField(
        upload_to="lms/pictures",
        verbose_name="Картинка",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    video_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Загрузите видео",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Укажите владельца урока",
        related_name='owned_lessons'
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
