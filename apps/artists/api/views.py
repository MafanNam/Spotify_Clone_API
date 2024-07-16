from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.artists.models import Artist, ArtistVerificationRequest, FavoriteArtist, License
from apps.core import filters, pagination
from apps.core.permissions import ArtistRequiredPermission, IsPremiumUserPermission

from .serializers import ArtistSerializer, FavoriteArtistSerializer, LicenseSerializer, UpdateArtistImageSerializer


class ArtistListCreateAPIView(generics.ListCreateAPIView):
    """
    Artist List Create API View. Create only for authenticated users.
    Only one artist can be created for each user.
    """

    queryset = Artist.objects.select_related("user").all()
    serializer_class = ArtistSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ArtistFilter
    search_fields = ["display_name", "first_name", "last_name"]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class ArtistDetailAPIView(generics.RetrieveAPIView):
    """
    Artist Detail API View. Public.
    """

    queryset = Artist.objects.select_related("user").all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class ArtistDetailMeAPIView(generics.RetrieveUpdateAPIView):
    """
    Artist Detail API View. Only for owner artist.
    """

    serializer_class = ArtistSerializer
    permission_classes = [ArtistRequiredPermission]

    def get_object(self):
        return self.request.user.artist


class MyArtistImageAPIView(generics.UpdateAPIView):
    """
    Update artist profile image. Only users can update their profile image.
    """

    permission_classes = [ArtistRequiredPermission]
    serializer_class = UpdateArtistImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.artist


class ArtistVerifyMeAPIView(views.APIView):
    """
    Artist Verify API View. Only for artist with premium.
    """

    permission_classes = [ArtistRequiredPermission, IsPremiumUserPermission]
    serializer_class = None

    def post(self, request):
        artist = request.user.artist
        ArtistVerificationRequest.objects.update_or_create(artist=artist, defaults={"is_processed": False})
        return Response({"msg": "Verification email will be sent in 24 hours."}, status=status.HTTP_200_OK)


class LicenseListCreateAPIView(generics.ListCreateAPIView):
    """
    License List Create API View. Create only for artist.
    """

    serializer_class = LicenseSerializer
    permission_classes = [ArtistRequiredPermission]

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)

    def get_queryset(self):
        return License.objects.select_related("artist").filter(artist=self.request.user.artist)


class LicenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    License Retrieve Update Destroy API View. Only for artist.
    """

    serializer_class = LicenseSerializer
    permission_classes = [ArtistRequiredPermission]

    def get_queryset(self):
        return License.objects.select_related("artist").filter(artist=self.request.user.artist)


class ArtistFavoriteListAPIView(generics.ListAPIView):
    """
    Favorite Artist List API View.
    Private view, only for authenticated users and owner.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteArtistSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.FavoriteArtistFilter
    search_fields = ["user__display_name", "artist__display_name"]
    ordering_fields = ["artist__created_at"]

    def get_queryset(self):
        return FavoriteArtist.objects.select_related("user", "artist", "artist__user").filter(user=self.request.user)


class ArtistFavoriteCreateAPIView(views.APIView):
    """
    Favorite Artist Create API View.
    Private view, only for authenticated users and owner.
    - `POST`: Add artist to favorites.
    1. If artist already in favorites, return `HTTP_400_BAD_REQUEST.
    2. If artist not in favorites, create new favorite and return `HTTP_201_CREATED`.
    - `DELETE`: Remove artist from favorites.
    1. If artist not in favorites, return `HTTP_404_NOT_FOUND`.
    2. If artist in favorites, delete favorite and return `HTTP_204_NO_CONTENT`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, *args, **kwargs):
        artist = get_object_or_404(Artist, slug=kwargs.get("slug"))
        favorite_playlist, created = FavoriteArtist.objects.get_or_create(user=request.user, artist=artist)
        if not created:
            return Response({"msg": "Artist already added to favorites"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Artist added to favorites"}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        artist = get_object_or_404(Artist, slug=kwargs.get("slug"))
        favorite_playlist = get_object_or_404(FavoriteArtist, user=request.user, artist=artist)
        favorite_playlist.delete()
        return Response({"msg": "Artist removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
