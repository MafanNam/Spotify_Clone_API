# Generated by Django 5.0.6 on 2024-07-21 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("playlists", "0009_alter_playlist_release_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="release_date",
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name="release date"),
        ),
    ]