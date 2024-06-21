from rest_framework import generics, permissions

from apps.analytics.models import PlaylistPlayed
from apps.core.permissions import IsOwnerUserPermission
from apps.playlists.api.serializers import PlaylistSerializer, ShortPlaylistSerializer
from apps.playlists.models import Playlist


class PlaylistListAPIView(generics.ListAPIView):
    """
    Playlist List API View. Public view.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortPlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(is_private=False)


class PlaylistDetailAPIView(generics.RetrieveAPIView):
    """
    Playlist Detail API View. Public view.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PlaylistSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Playlist.objects.filter(is_private=False)

    def retrieve(self, request, *args, **kwargs):
        playlist = self.get_object()
        viewer_ip = request.META.get("REMOTE_ADDR", None)

        PlaylistPlayed.record_listening(
            user=request.user if request.user.is_authenticated else None,
            playlist=playlist,
            viewer_ip=viewer_ip,
        )

        return super().retrieve(request, *args, **kwargs)


class PlaylistRecentlyPlayedAPIView(generics.ListAPIView):
    """
    List all recently played playlist. Public view.
    Filter last played 10 playlist by users or anonymous(by viewer IP).
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortPlaylistSerializer

    def get_queryset(self):
        viewer_ip = self.request.META.get("REMOTE_ADDR", None)

        if self.request.user.is_authenticated:
            return Playlist.objects.filter(is_private=False, playlist_plays__user=self.request.user).order_by(
                "-playlist_plays__played_at"
            )[:10]

        if viewer_ip:
            return Playlist.objects.filter(is_private=False, playlist_plays__viewer_ip=viewer_ip).order_by(
                "-playlist_plays__played_at"
            )[:10]

        return Playlist.objects.none()


class MyPlaylistListCreateAPIView(generics.ListCreateAPIView):
    """
    My Playlist List Create API View.
    Private view, only for authenticated users and owner.
    """

    permission_classes = [IsOwnerUserPermission]
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyPlaylistDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    My Playlist Detail API View.
    Private view, only for authenticated users and owner.
    """

    permission_classes = [IsOwnerUserPermission]
    serializer_class = PlaylistSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)
