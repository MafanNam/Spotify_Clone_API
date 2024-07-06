from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.albums.models import Album
from apps.artists.api.serializers import ShortArtistSerializer
from apps.audio.api.serializers import ShortTrackSerializer


class AlbumSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)
    # track_file = serializers.SerializerMethodField(read_only=True)
    track_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",
            "slug",
            "title",
            "artist",
            "track_slug",
            "image",
            "color",
            "is_private",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"color": {"read_only": True}}

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
    #     tracks = obj.tracks
    #     request = self.context.get("request")
    #     if tracks.exists():
    #         return request.build_absolute_uri(tracks.first().file.url)


class AlbumDetailSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)
    tracks = ShortTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",
            "slug",
            "title",
            "artist",
            "image",
            "color",
            "tracks",
            "is_private",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"color": {"read_only": True}}
