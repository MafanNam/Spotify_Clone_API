from django.contrib import admin

from apps.payments.models import Payment, Tax


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "method", "status", "price", "tax", "total_price"]
    list_display_links = ["id", "user"]
    list_filter = ["method", "status", "price", "tax", "total_price"]
    search_fields = ["user", "method", "status", "price"]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "value"]
    list_display_links = ["id", "name"]
    list_filter = ["name", "value"]
    search_fields = ["name", "value"]
