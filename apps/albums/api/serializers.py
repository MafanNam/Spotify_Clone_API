from rest_framework import serializers

from apps.albums.models import Album
from apps.artists.api.serializers import ShortArtistSerializer
from apps.audio.api.serializers import ShortTrackSerializer


class AlbumSerializer(serializers.ModelSerializer):
    artist = ShortArtistSerializer(read_only=True, many=False)

    class Meta:
        model = Album
        fields = [
            "id",
            "slug",
            "title",
            "artist",
            "image",
            "is_private",
            "created_at",
            "updated_at",
        ]


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
            "tracks",
            "is_private",
            "created_at",
            "updated_at",
        ]
