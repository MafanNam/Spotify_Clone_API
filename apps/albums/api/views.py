from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.albums.api.serializers import AlbumDetailSerializer, AlbumSerializer
from apps.albums.models import Album
from apps.core import filters, pagination
from apps.core.permissions import ArtistRequiredPermission


class AlbumListAPIView(generics.ListAPIView):
    """
    Album List API View. Public view.
    """

    serializer_class = AlbumSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.AlbumFilter
    search_fields = ["artist__display_name", "title", "tracks__title"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(is_private=False)


class AlbumDetailAPIView(generics.RetrieveAPIView):
    """
    Album Detail API View. Public view.
    """

    serializer_class = AlbumDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(is_private=False)


class MyAlbumListCreateAPIView(generics.ListCreateAPIView):
    """
    My Album List Create API View.
    Private view, only for authenticated users and owner.
    """

    serializer_class = AlbumDetailSerializer
    permission_classes = [ArtistRequiredPermission]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.MyAlbumFilter
    search_fields = ["artist__display_name", "title", "tracks__title"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(artist=self.request.user.artist)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)


class MyAlbumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    My Album Detail API View.
    Private view, only for authenticated users and owner.
    """

    serializer_class = AlbumSerializer
    permission_classes = [ArtistRequiredPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Album.objects.select_related("artist").filter(artist=self.request.user.artist)
