from django.contrib import admin

from apps.artists.models import Artist, ArtistVerificationRequest, FavoriteArtist, License


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "display_name", "image", "is_verify"]
    list_display_links = ["id", "user", "display_name"]
    list_editable = ["is_verify"]
    list_filter = ["is_verify"]


@admin.register(FavoriteArtist)
class FavoriteArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "artist", "created_at")
    list_display_links = ("id", "user", "artist")
    list_filter = ("created_at",)
    search_fields = ("user__display_name", "artist_display_name")


@admin.register(ArtistVerificationRequest)
class ArtistVerificationRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "artist", "is_processed", "created_at", "updated_at"]
    list_display_links = ["id", "artist"]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ["id", "artist", "name", "created_at", "updated_at"]
    list_display_links = ["id", "artist", "name"]
    list_filter = ["created_at", "updated_at"]
