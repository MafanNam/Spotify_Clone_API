# Generated by Django 5.0.6 on 2024-07-22 00:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("analytics", "0001_initial"),
        ("playlists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlistplayed",
            name="playlist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="playlist_plays", to="playlists.playlist"
            ),
        ),
    ]
