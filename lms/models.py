from django.db import models


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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
