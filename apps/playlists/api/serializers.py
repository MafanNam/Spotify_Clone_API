from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.audio.api.serializers import ShortTrackSerializer
from apps.other.api.serializers import GenreSerializer
from apps.playlists.models import FavoritePlaylist, Playlist
from apps.users.api.serializers import ShortCustomUserSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=False)
    tracks = ShortTrackSerializer(many=True, read_only=True)
    duration = serializers.DurationField(source="total_duration", read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "color",
            "user",
            "tracks",
            "genre",
            "release_date",
            "is_private",
            "duration",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"color": {"read_only": True}}


class ShortPlaylistSerializer(PlaylistSerializer):
    # track_file = serializers.SerializerMethodField(read_only=True)
    track_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "color",
            "track_slug",
            "user",
            "genre",
            "is_private",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_track_slug(self, obj):
        track = obj.tracks.first()
        if track:
            return track.slug

    # @extend_schema_field(ShortTrackSerializer)
    # def get_first_track(self, obj):
    #     track = obj.tracks.first()
    #     if track:
    #         return ShortTrackSerializer(track).data

    # @extend_schema_field(OpenApiTypes.URI_REF)
    # def get_track_file(self, obj):
    #     track = obj.tracks.first()
    #     request = self.context.get("request")
    #     if track:
    #         return request.build_absolute_uri(track.file.url)


class FavoritePlaylistSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)
    playlist = ShortPlaylistSerializer(read_only=True, many=False)

    class Meta:
        model = FavoritePlaylist
        fields = ["id", "user", "playlist", "created_at", "updated_at"]
