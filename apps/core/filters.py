import django_filters

from apps.albums.models import Album
from apps.artists.models import Artist
from apps.audio.models import Track
from apps.payments.models import Payment
from apps.playlists.models import FavoritePlaylist, Playlist


class TrackFilter(django_filters.FilterSet):
    class Meta:
        model = Track
        fields = {
            "genre__slug": ["exact"],
            "artist__slug": ["exact"],
            "album__slug": ["exact"],
        }


class MyTrackFilter(django_filters.FilterSet):
    class Meta:
        model = Track
        fields = {
            "genre__slug": ["exact"],
            "album__slug": ["exact"],
            "is_private": ["exact"],
        }


class ArtistFilter(django_filters.FilterSet):
    class Meta:
        model = Artist
        fields = {
            "is_verify": ["exact"],
        }


class AlbumFilter(django_filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            "is_private": ["exact"],
            "artist__slug": ["exact"],
        }


class MyAlbumFilter(django_filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            "is_private": ["exact"],
        }


class PlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = Playlist
        fields = {
            "genre__slug": ["exact"],
            "user__id": ["exact"],
            "tracks__slug": ["exact"],
        }


class MyPlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = Playlist
        fields = {
            "genre__slug": ["exact"],
            "user__id": ["exact"],
            "tracks__slug": ["exact"],
            "is_private": ["exact"],
        }


class FavoritePlaylistFilter(django_filters.FilterSet):
    class Meta:
        model = FavoritePlaylist
        fields = {
            "playlist__genre__slug": ["exact"],
            "user__id": ["exact"],
            "playlist__tracks__slug": ["exact"],
        }


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            "status": ["exact"],
            "method": ["exact"],
            "price": ["exact", "gte", "lte", "range"],
            "total_price": ["exact", "gte", "lte", "range"],
        }
