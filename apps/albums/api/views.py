from rest_framework import generics, permissions

from apps.albums.api.serializers import AlbumDetailSerializer, AlbumSerializer
from apps.albums.models import Album
from apps.core.permissions import ArtistRequiredPermission


class AlbumListCreateAPIView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Album.objects.filter(is_private=False)


class AlbumDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AlbumDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.filter(is_private=False)


class MyAlbumListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AlbumDetailSerializer
    permission_classes = [ArtistRequiredPermission]

    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user.artist)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)


class MyAlbumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [ArtistRequiredPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user.artist)
