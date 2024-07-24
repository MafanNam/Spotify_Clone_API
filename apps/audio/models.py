from datetime import date, timedelta

from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from mutagen import File

from apps.albums.models import Album
from apps.artists.models import Artist, License
from apps.core.models import TimeStampedModel
from apps.core.services import (
    generate_color_from_image,
    get_path_upload_image_track,
    get_path_upload_track,
    validate_image_size,
    validate_track_size,
)
from apps.other.models import Genre

User = get_user_model()


class Track(TimeStampedModel):
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="tracks",
        verbose_name=_("artist"),
        default="",
    )
    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True)
    duration = models.DurationField(_("duration"), null=True, blank=True)
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_track,
        validators=[validate_image_size],
        blank=True,
        default="default/track.jpg",
    )
    color = ColorField(default="#202020")
    license = models.ForeignKey(
        License,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracks",
        verbose_name=_("license"),
        default="",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracks",
        verbose_name=_("genre"),
        default="",
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracks",
        verbose_name=_("album"),
        default="",
    )
    file = models.FileField(
        verbose_name=_("file track"),
        upload_to=get_path_upload_track,
        validators=[validate_track_size],
    )
    plays_count = models.PositiveBigIntegerField(_("plays count"), default=0)
    downloads_count = models.PositiveBigIntegerField(_("downloads count"), default=0)
    likes_count = models.PositiveBigIntegerField(_("likes count"), default=0)
    user_of_likes = models.ManyToManyField(
        User,
        related_name="liked_tracks",
        verbose_name=_("user of likes"),
        blank=True,
    )
    is_private = models.BooleanField(_("is private"), default=False)
    release_date = models.DateField(
        _("release date"),
        null=True,
        blank=True,
        default=date.today,
    )

    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        if self.file:
            audio = File(self.file)
            if audio is not None:
                self.duration = timedelta(seconds=audio.info.length)
        if self.image:
            self.color = generate_color_from_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
