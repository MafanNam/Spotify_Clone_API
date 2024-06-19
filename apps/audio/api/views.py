import os.path

from django.http import FileResponse, Http404
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from apps.analytics.models import TrackPlayed
from apps.audio.api.serializers import ShortTrackSerializer, TrackCreateSerializer, TrackSerializer
from apps.audio.models import Track
from apps.core.permissions import ArtistRequiredPermission


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
        return get_object_or_404(Track, slug=self.kwargs.get("slug"), is_private=False, artist=self.request.user.artist)
