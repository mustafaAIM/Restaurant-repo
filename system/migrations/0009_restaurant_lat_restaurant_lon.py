# Generated by Django 5.0.6 on 2024-07-04 17:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system", "0008_booking_guests_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="lat",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="lon",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]