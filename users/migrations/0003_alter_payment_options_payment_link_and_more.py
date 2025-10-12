import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payment",
            options={"verbose_name": "Платеж", "verbose_name_plural": "Платежи"},
        ),
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.URLField(
                blank=True, max_length=400, null=True, verbose_name="Ссылка на оплату"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="id сессии"
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="amount",
            field=models.PositiveIntegerField(verbose_name="Сумма оплаты"),
        ),
        migrations.AlterField(
            model_name="payment",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
