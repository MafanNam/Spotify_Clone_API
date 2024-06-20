from rest_framework import serializers

from apps.audio.api.serializers import ShortTrackSerializer
from apps.other.api.serializers import GenreSerializer
from apps.playlists.models import Playlist
from apps.users.api.serializers import ShortCustomUserSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    user = ShortCustomUserSerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=False)
    tracks = ShortTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "user",
            "tracks",
            "genre",
            "release_date",
            "is_private",
            "created_at",
            "updated_at",
        ]


class ShortPlaylistSerializer(PlaylistSerializer):
    class Meta:
        model = Playlist
        fields = [
            "id",
            "slug",
            "title",
            "image",
            "user",
            "genre",
            "is_private",
        ]
