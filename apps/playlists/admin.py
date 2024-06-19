from django.contrib import admin

from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "release_date", "is_private")
    list_display_links = ("id", "user", "title")
    list_editable = ("is_private",)
    list_filter = ("is_private", "release_date")
    search_fields = ("title", "user__display_name", "genre__name")
