from rest_framework import generics, permissions

from apps.other.api.serializers import GenreSerializer
from apps.other.models import Genre


class GenreListAPIView(generics.ListCreateAPIView):
    """
    API endpoint that allows genres to be viewed.
    Admin can create new genre.
    All users can see all genres.
    Color field generates on image.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class GenreDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows genres details to be viewed.
    Admin can update and delete genre.
    Color field generates on image.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
