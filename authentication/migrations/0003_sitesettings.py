# Generated by Django 5.0.6 on 2024-07-13 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_alter_user_birth_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
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
                    "email",
                    models.EmailField(
                        help_text="The email address for the site.", max_length=254
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        help_text="The phone number for the site.", max_length=20
                    ),
                ),
                (
                    "facebook_url",
                    models.URLField(help_text="The Facebook URL for the site."),
                ),
                (
                    "terms_and_conditions",
                    models.TextField(
                        help_text="The terms and conditions for the site."
                    ),
                ),
                (
                    "privacy_policy",
                    models.TextField(help_text="The privacy policy for the site."),
                ),
            ],
        ),
    ]
