from django.contrib import admin

from .models import PlaylistPlayed, Similarity, TrackPlayed


@admin.register(Similarity)
class SimilarityAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "track", "score")
    list_display_links = ("id", "user")
    list_filter = ("score", "created_at")
    search_fields = ("user__display_name", "track__title")
    ordering = ("-score", "-created_at")


@admin.register(TrackPlayed)
class TrackPlayedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "track", "viewer_ip")
    list_display_links = ("id", "user")
    list_filter = ("viewer_ip", "created_at")
    search_fields = ("user__display_name", "track__title")
    ordering = ("-created_at",)


@admin.register(PlaylistPlayed)
class PlaylistPlayedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "playlist", "viewer_ip", "played_at")
    list_display_links = ("id", "user")
    list_filter = ("viewer_ip", "created_at")
    search_fields = ("user__display_name", "playlist__title")
    ordering = (
        "-played_at",
        "-created_at",
    )
