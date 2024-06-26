from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.audio.models import Track
from apps.core.models import TimeStampedModel
from apps.playlists.models import Playlist

User = get_user_model()


class Similarity(TimeStampedModel):
    """
    Similarity model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="similarities")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="similarities")
    score = models.DecimalField(_("score"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Similarity")
        verbose_name_plural = _("Similarities")
        unique_together = ("user", "track")

    def __str__(self):
        return f"{self.user} - {self.track} - {self.score}"


class TrackPlayed(TimeStampedModel):
    """
    Track played model.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="plays")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="plays")
    viewer_ip = models.GenericIPAddressField(_("viewer IP"), blank=True, null=True)
    played_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Track Play")
        verbose_name_plural = _("Track Plays")
        unique_together = ("user", "track", "viewer_ip")

    def __str__(self):
        return f"{self.track.title} listed by {self.user.display_name if self.user else 'Anonymous'} from IP {self.viewer_ip} at {self.played_at}"

    @classmethod
    def record_listening(cls, track, user, viewer_ip):
        view, _ = cls.objects.get_or_create(track=track, user=user, viewer_ip=viewer_ip)
        view.played_at = timezone.now()
        view.save()


class PlaylistPlayed(TimeStampedModel):
    """
    Playlist played model.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="playlist_plays")
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="playlist_plays")
    viewer_ip = models.GenericIPAddressField(_("viewer IP"), blank=True, null=True)
    played_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Playlist Play")
        verbose_name_plural = _("Playlist Plays")
        unique_together = ("user", "playlist", "viewer_ip")

    def __str__(self):
        return f"{self.playlist.title} listed by {self.user.display_name if self.user else 'Anonymous'} from IP {self.viewer_ip} at {self.played_at}"

    @classmethod
    def record_listening(cls, playlist, user, viewer_ip):
        view, _ = cls.objects.get_or_create(playlist=playlist, user=user, viewer_ip=viewer_ip)
        view.played_at = timezone.now()
        view.save()
