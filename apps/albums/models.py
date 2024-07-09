from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.artists.models import Artist
from apps.core.models import TimeStampedModel
from apps.core.services import generate_color_from_image, get_path_upload_image_album, validate_image_size


class Album(TimeStampedModel):
    """
    Album model.
    """

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name=_("artist"),
        default="",
    )
    title = models.CharField(_("title"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_album,
        validators=[validate_image_size],
        blank=True,
        default="default/album.jpg",
    )
    color = ColorField(default="#202020")
    is_private = models.BooleanField(_("is_private"), default=False)

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            self.color = generate_color_from_image(self.image)
        super().save(*args, **kwargs)
        # if generate_color:
        #     from apps.albums.tasks import generate_album_color
        #     generate_album_color.delay(self.id)
