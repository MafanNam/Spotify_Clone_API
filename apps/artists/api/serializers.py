from rest_framework import serializers

from apps.artists.models import Artist, License
from apps.users.api.serializers import ShortCustomUserSerializer


class ArtistSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)

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
            "is_verify",
        ]
        extra_kwargs = {"is_verify": {"read_only": True}}


class ShortArtistSerializer(ArtistSerializer):
    class Meta:
        model = Artist
        fields = ["id", "slug", "display_name", "image", "is_verify"]


class LicenseSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)

    class Meta:
        model = License
        fields = ["id", "artist", "name", "text"]
