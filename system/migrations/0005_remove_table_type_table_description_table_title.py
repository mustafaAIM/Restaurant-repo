# Generated by Django 5.0.6 on 2024-07-02 18:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0004_alter_dish_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="table",
            name="type",
        ),
        migrations.AddField(
            model_name="table",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="table",
            name="title",
            field=models.TextField(default=""),
        ),
    ]
