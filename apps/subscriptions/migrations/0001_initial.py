# Generated by Django 5.0.6 on 2024-07-22 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("permission", models.CharField(max_length=255, verbose_name="Permission")),
            ],
            options={
                "verbose_name": "Feature",
                "verbose_name_plural": "Features",
            },
        ),
        migrations.CreateModel(
            name="SubscriptionPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Name")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Price")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                ("days_exp", models.PositiveIntegerField(default=0, verbose_name="Days expiration")),
                (
                    "feature",
                    models.ManyToManyField(blank=True, related_name="subscription_plan", to="subscriptions.feature"),
                ),
            ],
            options={
                "verbose_name": "Subscription plan",
                "verbose_name_plural": "Subscription plans",
            },
        ),
    ]
