import os.path

from django.http import FileResponse, Http404
from rest_framework import generics, permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.analytics.models import TrackPlayed
from apps.audio.api.serializers import ShortTrackSerializer, TrackCreateSerializer, TrackSerializer
from apps.audio.models import Track
from apps.core.permissions import ArtistRequiredPermission, IsPremiumUserPermission


class TrackListAPIView(generics.ListAPIView):
    """
    Track list. Public permission.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortTrackSerializer

    def get_queryset(self):
        return Track.objects.select_related("artist", "license", "genre", "album").filter(is_private=False)


class TrackLikedListAPIView(generics.ListAPIView):
    """
    Track liked list. Private permission.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShortTrackSerializer

    def get_queryset(self):
        return Track.objects.select_related("artist", "license", "genre", "album").filter(
            user_of_likes=self.request.user
        )


class TrackDetailAPIView(generics.RetrieveAPIView):
    """
    Track detail. Public permission.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = TrackSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Track.objects.select_related("artist", "license", "genre", "album").filter(is_private=False)


class TrackRecentlyPlayedAPIView(generics.ListAPIView):
    """
    List all recently played track. Public view.
    Filter last played 10 tracks by users or anonymous(by viewer IP).
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortTrackSerializer

    def get_queryset(self):
        viewer_ip = self.request.META.get("REMOTE_ADDR", None)

        if self.request.user.is_authenticated:
            return (
                Track.objects.select_related("artist", "license", "genre", "album")
                .filter(is_private=False, plays__user=self.request.user)
                .order_by("-plays__played_at")[:10]
            )

        if viewer_ip:
            return (
                Track.objects.select_related("artist", "license", "genre", "album")
                .filter(is_private=False, plays__viewer_ip=viewer_ip)
                .order_by("-plays__played_at")[:10]
            )

        return Track.objects.none()


class TrackMyListCreateAPIView(generics.ListCreateAPIView):
    """
    List all my tracks.
    Only for authenticated user(artist).
    """

    permission_classes = [ArtistRequiredPermission]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TrackCreateSerializer
        return TrackSerializer

    def get_queryset(self):
        return (
            Track.objects.select_related("artist", "genre", "license", "album")
            .prefetch_related("license__artist", "user_of_likes")
            .filter(artist=self.request.user.artist)
        )

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)


class TrackMyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Track detail. Only for authenticated user(artist).
    """

    permission_classes = [ArtistRequiredPermission]
    serializer_class = TrackCreateSerializer
    lookup_field = "slug"

    def get_object(self):
        return (
            Track.objects.select_related("artist")
            .prefetch_related("user_of_likes")
            .get(slug=self.kwargs.get("slug"), artist=self.request.user.artist)
        )


class StreamingTrackAPIView(views.APIView):
    """Listen track. Public permission."""

    serializer_class = None
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    @staticmethod
    def set_play(track):
        track.plays_count += 1
        track.save()

    def get(self, request, *args, **kwargs):
        track = self.get_object()
        viewer_ip = request.META.get("REMOTE_ADDR", None)

        if os.path.exists(track.file.path):
            self.set_play(track)
            TrackPlayed.record_listening(
                user=request.user if request.user.is_authenticated else None,
                track=track,
                viewer_ip=viewer_ip,
            )

            return FileResponse(open(track.file.path, "rb"), filename=track.file.name)
        else:
            return Http404


class StreamingMyTrackAPIView(StreamingTrackAPIView):
    """
    Listen my track. Only for authenticated user(artist).
    """

    permission_classes = [ArtistRequiredPermission]
    http_method_names = ["get"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), artist=self.request.user.artist)


class DownloadTrackAPIView(views.APIView):
    """Download track. Only for premium user."""

    serializer_class = None
    permission_classes = [IsPremiumUserPermission]
    http_method_names = ["get"]

    @staticmethod
    def set_download(track):
        track.downloads_count += 1
        track.save()

    def get(self, request, *args, **kwargs):
        track = get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)
        if os.path.exists(track.file.path):
            self.set_download(track)
            return FileResponse(
                open(track.file.path, "rb"),
                filename=track.file.name,
                as_attachment=True,
            )
        else:
            return Http404


class TrackLikeAPIView(views.APIView):
    """
    Like track. Only for authenticated user.
    - If user has not liked the track, add the like and increase the likes count and return status `HTTP_200_OK`.
    - If user has already liked the track, return a message and status `HTTP_400_BAD_REQUEST`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    http_method_names = ["post"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    def post(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user not in track.user_of_likes.all():
            track.likes_count += 1
            track.user_of_likes.add(request.user)
            track.save()
            return Response({"likes_count": track.likes_count}, status.HTTP_200_OK)
        # If user has already liked the track, return a message
        return Response({"msg": "You have already liked this track."}, status=status.HTTP_400_BAD_REQUEST)


class TrackUnlikeAPIView(views.APIView):
    """
    Unlike track. Only for authenticated user.
    - If user has not liked the track, return a message and status `HTTP_400_BAD_REQUEST`.
    - If user has liked the track, remove the like and decrease the likes count and return status `HTTP_200_OK`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    http_method_names = ["delete"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    def delete(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user in track.user_of_likes.all():
            track.user_of_likes.remove(request.user)
            track.likes_count -= 1
            track.save()
            return Response({"likes_count": track.likes_count}, status.HTTP_200_OK)
        return Response({"msg": "You have not liked this track."}, status=status.HTTP_400_BAD_REQUEST)
