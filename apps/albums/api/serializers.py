from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.albums.models import Album, FavoriteAlbum
from apps.artists.api.serializers import ShortArtistSerializer
from apps.audio.api.serializers import ShortTrackSerializer


class AlbumSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)
    track_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "artist",
            "track_slug",
            "image",
            "color",
            "is_private",
            "release_date",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"color": {"read_only": True}}

    @extend_schema_field(OpenApiTypes.STR)
    def get_track_slug(self, obj):
        track = obj.tracks.first()
        if track:
            return track.slug


class AlbumDetailSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)
    tracks = ShortTrackSerializer(many=True, read_only=True)
    duration = serializers.DurationField(source="total_duration", read_only=True)
    album_listeners = serializers.IntegerField(source="get_tracks_listeners", read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "artist",
            "album_listeners",
            "image",
            "color",
            "tracks",
            "duration",
            "is_private",
            "release_date",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"color": {"read_only": True}}


class FavoriteAlbumSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True, many=False)

    class Meta:
        model = FavoriteAlbum
        fields = ["id", "album", "created_at", "updated_at"]
