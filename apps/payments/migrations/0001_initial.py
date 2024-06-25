# Generated by Django 5.0.6 on 2024-06-24 10:00

import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("payment_id", shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                (
                    "method",
                    models.CharField(
                        choices=[("paypal", "PayPal"), ("stripe", "Stripe")],
                        default="paypal",
                        max_length=50,
                        verbose_name="Payment Method",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("success", "Success"),
                            ("failed", "Failed"),
                            ("canceled", "Canceled"),
                            ("refunded", "Refunded"),
                        ],
                        default="pending",
                        max_length=50,
                        verbose_name="Payment Status",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Price")),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Total Price"),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
            },
        ),
        migrations.CreateModel(
            name="Tax",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="Tax Name")),
                ("value", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Tax")),
            ],
            options={
                "verbose_name": "Tax",
                "verbose_name_plural": "Taxes",
            },
        ),
    ]
