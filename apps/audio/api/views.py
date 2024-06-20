import os.path

from django.http import FileResponse, Http404
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.analytics.models import TrackPlayed
from apps.audio.api.serializers import ShortTrackSerializer, TrackCreateSerializer, TrackSerializer
from apps.audio.models import Track
from apps.core.permissions import ArtistRequiredPermission, IsPremiumUserPermission


class TrackListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShortTrackSerializer

    def get_queryset(self):
        return Track.objects.filter(is_private=False)


class TrackDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TrackSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Track.objects.filter(is_private=False)


class TrackRecentlyPlayedAPIView(generics.ListAPIView):
    """List all recently played track"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShortTrackSerializer

    def get_queryset(self):
        return Track.objects.filter(private=False, plays__user=self.request.user).order_by("-plays__played_at")[:10]


class TrackMyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [ArtistRequiredPermission]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TrackCreateSerializer
        return TrackSerializer

    def get_queryset(self):
        return Track.objects.filter(artist=self.request.user.artist)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user.artist)


class TrackMyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ArtistRequiredPermission]
    serializer_class = TrackCreateSerializer
    lookup_field = "slug"

    def get_object(self):
        return Track.objects.get(slug=self.kwargs.get("slug"), artist=self.request.user.artist)


class StreamingTrackAPIView(generics.RetrieveAPIView):
    """Listen track"""

    serializer_class = None
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    @staticmethod
    def set_play(track):
        track.plays_count += 1
        track.save()

    def retrieve(self, request, *args, **kwargs):
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
    permission_classes = [ArtistRequiredPermission]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), artist=self.request.user.artist)


class DownloadTrackAPIView(generics.RetrieveAPIView):
    """Download track. Only for premium users"""

    serializer_class = None
    permission_classes = [IsPremiumUserPermission]

    @staticmethod
    def set_download(track):
        track.downloads_count += 1
        track.save()

    def retrieve(self, request, *args, **kwargs):
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


class TrackLikeAPIView(generics.UpdateAPIView):
    """Like track. Only for premium users"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    lookup_field = "slug"
    http_method_names = ["patch"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    def patch(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user not in track.user_of_likes.all():
            track.likes_count += 1
            track.user_of_likes.add(request.user)
            track.save()
            return Response({"likes_count": track.likes_count}, status.HTTP_200_OK)
        # If user has already liked the track, return a message
        return Response({"detail": "You have already liked this track."}, status=status.HTTP_400_BAD_REQUEST)


class TrackUnlikeAPIView(generics.UpdateAPIView):
    """Unlike track. Only for premium users"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    lookup_field = "slug"
    http_method_names = ["patch"]

    def get_object(self):
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False)

    def patch(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user in track.user_of_likes.all():
            track.user_of_likes.remove(request.user)
            track.likes_count -= 1
            track.save()
            return Response({"likes_count": track.likes_count}, status.HTTP_200_OK)
        return Response({"detail": "You have not liked this track."}, status=status.HTTP_400_BAD_REQUEST)
