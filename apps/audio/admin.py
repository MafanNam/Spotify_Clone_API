from django.contrib import admin

from .models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "artist",
        "album",
        "duration",
        "license",
        "genre",
        "is_private",
        "release_date",
    )
    list_editable = (
        "is_private",
        "release_date",
    )
    list_display_links = ("id", "title")
    list_filter = ("is_private", "release_date")
    ordering = ("-release_date",)
    search_fields = ("title", "artist__name")
