from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_payment_options_payment_link_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("BANK_TRANSFER", "Банковский перевод"),
                    ("CASH", "Наличными"),
                ],
                max_length=100,
                null=True,
                verbose_name="Cпособ оплаты",
            ),
        ),
    ]
