from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.artists.models import Artist, License
from apps.audio.models import Track
from apps.users.api.serializers import ShortCustomUserSerializer


class ArtistSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)
    # track_file = serializers.SerializerMethodField(read_only=True)
    track_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artist
        fields = [
            "id",
            "slug",
            "user",
            "first_name",
            "last_name",
            "display_name",
            "image",
            "color",
            "track_slug",
            "is_verify",
        ]
        extra_kwargs = {"is_verify": {"read_only": True}, "color": {"read_only": True}}

    @extend_schema_field(OpenApiTypes.STR)
    def get_track_slug(self, obj):
        track = Track.objects.filter(artist=obj).first()
        if track:
            return track.slug

    # @extend_schema_field(ShortTrackSerializer)
    # def get_first_track(self, obj):
    #     track = Track.objects.filter(artist=obj).first()
    #     if track:
    #         return ShortTrackSerializer(track).data

    # @extend_schema_field(OpenApiTypes.URI_REF)
    # def get_track_file(self, obj):
    #     track = Track.objects.filter(artist=obj).first()
    #     request = self.context.get("request")
    #     if track:
    #         return request.build_absolute_uri(track.file.url)


class ShortArtistSerializer(ArtistSerializer):
    class Meta:
        model = Artist
        fields = ["id", "slug", "display_name", "image", "color", "is_verify"]


class LicenseSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)

    class Meta:
        model = License
        fields = ["id", "artist", "name", "text"]
