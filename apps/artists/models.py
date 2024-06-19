from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.core.services import get_path_upload_image_artist, validate_image_size

User = get_user_model()


class Artist(TimeStampedModel):
    """
    Artist model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist")
    first_name = models.CharField(verbose_name=_("first name"), max_length=100)
    last_name = models.CharField(verbose_name=_("last name"), max_length=100)
    display_name = models.CharField(
        verbose_name=_("display name"),
        max_length=100,
        blank=True,
        unique=True,
        db_index=True,
    )
    slug = AutoSlugField(populate_from="display_name", unique=True)
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_artist,
        validators=[validate_image_size],
        blank=True,
        default="default/artist.jpg",
    )
    is_verify = models.BooleanField(_("is verify"), default=False)

    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")
        ordering = ["-created_at", "-updated_at"]

    def save(self, *args, **kwargs):
        if self.display_name == "" or self.display_name is None:
            self.display_name = f"{self.first_name} {self.last_name}"
        super(Artist, self).save(*args, **kwargs)

    def __str__(self):
        """String representation of the artist."""
        return self.display_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class License(TimeStampedModel):
    """
    License model.
    """

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="licenses")
    name = models.CharField(verbose_name=_("name"), max_length=255)
    text = models.TextField(verbose_name=_("text"), max_length=1000)

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        """String representation of the license."""
        return self.name
