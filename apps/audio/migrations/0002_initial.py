# Generated by Django 5.0.6 on 2024-07-22 00:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("audio", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="track",
            name="user_of_likes",
            field=models.ManyToManyField(
                blank=True, related_name="liked_tracks", to=settings.AUTH_USER_MODEL, verbose_name="user of likes"
            ),
        ),
    ]
