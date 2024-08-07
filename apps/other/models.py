from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.core.services import generate_color_from_image, get_path_upload_image_genre, validate_image_size


class Genre(TimeStampedModel):
    name = models.CharField(_("name"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_genre,
        validators=[validate_image_size],
        blank=True,
        default="default/track.jpg",
    )
    color = ColorField(default="#202020")

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            self.color = generate_color_from_image(self.image)
        super().save(*args, **kwargs)
