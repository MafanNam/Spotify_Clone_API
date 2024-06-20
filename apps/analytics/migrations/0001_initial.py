# Generated by Django 5.0.6 on 2024-06-18 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Similarity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("score", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="score")),
            ],
            options={
                "verbose_name": "similarity",
                "verbose_name_plural": "similarities",
            },
        ),
        migrations.CreateModel(
            name="TrackPlays",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("viewer_ip", models.GenericIPAddressField(blank=True, null=True, verbose_name="viewer IP")),
            ],
            options={
                "verbose_name": "track play",
                "verbose_name_plural": "track plays",
            },
        ),
    ]