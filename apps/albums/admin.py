from django.contrib import admin

from ..audio.models import Track
from .models import Album


class TrackInline(admin.TabularInline):
    model = Track


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "artist", "title", "is_private", "created_at", "updated_at")
    list_display_links = ("id", "artist")
    list_editable = ("is_private",)
    list_filter = ("is_private",)
    ordering = ("-created_at", "-updated_at")
    search_fields = ("title", "artist__display_name")

    inlines = [TrackInline]
