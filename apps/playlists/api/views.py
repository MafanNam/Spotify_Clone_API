from rest_framework import generics, permissions

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
