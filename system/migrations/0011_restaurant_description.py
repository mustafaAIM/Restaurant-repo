# Generated by Django 5.0.6 on 2024-07-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0010_alter_restaurant_work_from_alter_restaurant_work_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="description",
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
