# Generated by Django 5.0.6 on 2024-07-10 21:31

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="color",
            field=colorfield.fields.ColorField(default="#202020", image_field=None, max_length=25, samples=None),
        ),
    ]