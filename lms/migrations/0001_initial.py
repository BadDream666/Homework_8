import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название курса",
                        max_length=100,
                        verbose_name="Название курса",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Опишите курс",
                        max_length=250,
                        null=True,
                        verbose_name="Описание курса",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите превью",
                        null=True,
                        upload_to="lms/previews",
                        verbose_name="Превью",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название урока",
                        max_length=100,
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Опишите урок",
                        max_length=250,
                        null=True,
                        verbose_name="Описание урока",
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите картинку",
                        null=True,
                        upload_to="lms/pictures",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "video_link",
                    models.URLField(
                        blank=True,
                        help_text="Загрузите видео",
                        null=True,
                        verbose_name="Ссылка на видео",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        help_text="Выберите курс",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
