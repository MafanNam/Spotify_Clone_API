from django.contrib import admin

from .models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "color", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["-created_at", "-updated_at"]
