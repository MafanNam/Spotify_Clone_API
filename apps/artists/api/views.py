from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from apps.artists.models import Artist, ArtistVerificationRequest, License
from apps.core.permissions import ArtistRequiredPermission, IsPremiumUserPermission

from .serializers import ArtistSerializer, LicenseSerializer


class ArtistListCreateAPIView(generics.ListCreateAPIView):
    """
    Artist List Create API View. Create only for authenticated users.
    Only one artist can be created for each user.
    """

    queryset = Artist.objects.select_related("user").all()
    serializer_class = ArtistSerializer

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
