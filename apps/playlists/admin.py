from django.contrib import admin

from .models import FavoritePlaylist, Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "release_date", "is_private")
    list_display_links = ("id", "user", "title")
    list_editable = ("is_private",)
    list_filter = ("is_private", "release_date")
    search_fields = ("title", "user__display_name", "genre__name")


@admin.register(FavoritePlaylist)
class FavoritePlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "playlist", "created_at")
    list_display_links = ("id", "user", "playlist")
    list_filter = ("created_at",)
    search_fields = ("user__display_name", "playlist__title")
