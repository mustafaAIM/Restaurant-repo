# Generated by Django 5.0.6 on 2024-09-15 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0016_favorite"),
    ]

    operations = [
        migrations.CreateModel(
            name="Offer",
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
                ("discount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("end_at", models.DateField()),
                (
                    "dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="system.dish"
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="system.restaurant",
                    ),
                ),
            ],
        ),
    ]
