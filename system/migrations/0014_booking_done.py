# Generated by Django 5.0.6 on 2024-07-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0013_restaurant_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="done",
            field=models.BooleanField(default=False),
        ),
    ]