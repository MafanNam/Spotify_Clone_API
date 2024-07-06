from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.audio.models import Track
from apps.core.models import TimeStampedModel
from apps.core.services import get_path_upload_image_playlist, validate_image_size
from apps.other.models import Genre

User = get_user_model()


class Playlist(TimeStampedModel):
    """
    Playlist model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    tracks = models.ManyToManyField(Track, related_name="playlists")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="playlists")
    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True)
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_playlist,
        validators=[validate_image_size],
        blank=True,
        default="default/track.jpg",
    )
    color = ColorField(image_field="image")
    release_date = models.DateField(_("release date"), blank=True, null=True, default=timezone.now)
    is_private = models.BooleanField(_("is_private"), default=False)

    @property
    def get_tracks_count(self):
        return self.tracks.count()

    @property
    def get_tracks(self):
        return self.tracks.all()

    @property
    def total_duration(self):
        total_duration = self.tracks.aggregate(total_duration=Sum("duration"))["total_duration"]
        return total_duration

    class Meta:
        verbose_name = _("Playlist")
        verbose_name_plural = _("Playlists")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.title


class FavoritePlaylist(TimeStampedModel):
    """
    Favorite playlist model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_playlists")
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="favorite_playlists")

    class Meta:
        verbose_name = _("Favorite playlist")
        verbose_name_plural = _("Favorite playlists")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return f"{self.user} is favorite {self.playlist.title}"
