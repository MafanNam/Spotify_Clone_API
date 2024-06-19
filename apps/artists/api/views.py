from rest_framework import generics, permissions

from apps.artists.models import Artist, License
from apps.core.permissions import ArtistRequiredPermission

from .serializers import ArtistSerializer, LicenseSerializer


class ArtistListCreateAPIView(generics.ListCreateAPIView):
    """
    Artist List Create API View. Create only for authenticated users.
    Only one artist can be created for each user.
    """

    queryset = Artist.objects.all()
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

    queryset = Artist.objects.all()
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


# class ArtistVerifyMeAPIView(generics.UpdateAPIView):
#     """
#     Artist Verify API View. Only for owner artist.
#     """
#
#     serializer_class = ArtistSerializer
#     permission_classes = [ArtistRequiredPermission]
#
#     def get_object(self):
#         return self.request.user.artist
#
#     def perform_update(self, serializer):
#         serializer.save(is_verify=True)


class LicenseListCreateAPIView(generics.ListCreateAPIView):
    """
    License List Create API View. Create only for artist.
    """

    serializer_class = LicenseSerializer
    permission_classes = [ArtistRequiredPermission]

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)

    def get_queryset(self):
        return License.objects.filter(artist=self.request.user.artist)


class LicenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    License Retrieve Update Destroy API View. Only for artist.
    """

    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [ArtistRequiredPermission]

    def get_queryset(self):
        return self.queryset.filter(artist=self.request.user.artist)
