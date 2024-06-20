# Generated by Django 5.0.6 on 2024-06-19 18:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0003_initial"),
        ("audio", "0003_alter_track_file"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TrackPlayed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("viewer_ip", models.GenericIPAddressField(blank=True, null=True, verbose_name="viewer IP")),
                ("played_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="plays", to="audio.track"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="plays",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "track play",
                "verbose_name_plural": "track plays",
                "unique_together": {("user", "track", "viewer_ip")},
            },
        ),
        migrations.DeleteModel(
            name="TrackPlays",
        ),
    ]