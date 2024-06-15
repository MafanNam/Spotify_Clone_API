from django.contrib import admin

from .models import Feature, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "days_exp"]
    list_display_links = ["id", "name"]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "permission"]
    list_display_links = ["id", "name"]
