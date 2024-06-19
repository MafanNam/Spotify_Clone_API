# Generated by Django 5.0.6 on 2024-06-18 20:42

import apps.core.services
import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=100, verbose_name="first name")),
                ("last_name", models.CharField(max_length=100, verbose_name="last name")),
                (
                    "display_name",
                    models.CharField(
                        blank=True, db_index=True, max_length=100, unique=True, verbose_name="display name"
                    ),
                ),
                ("slug", autoslug.fields.AutoSlugField(editable=False, populate_from="display_name", unique=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="default/artist.jpg",
                        upload_to=apps.core.services.get_path_upload_image_artist,
                        validators=[apps.core.services.validate_image_size],
                        verbose_name="image",
                    ),
                ),
                ("is_verify", models.BooleanField(default=False, verbose_name="is verify")),
            ],
            options={
                "verbose_name": "Artist",
                "verbose_name_plural": "Artists",
                "ordering": ["-created_at", "-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("text", models.TextField(max_length=1000, verbose_name="text")),
            ],
            options={
                "verbose_name": "License",
                "verbose_name_plural": "Licenses",
                "ordering": ["-created_at", "-updated_at"],
            },
        ),
    ]
