from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from model_utils import Choices

from apps.core.services import get_path_upload_image_artist, get_path_upload_image_user, validate_image_size

from ..core.models import TimeStampedModel
from ..subscriptions.models import SubscriptionPlan
from .managers import CustomUserManager

TYPE_PROFILE_CHOICES = Choices(
    ("user", _("User")),
    ("artist", _("Artist")),
)

GENDER_CHOICES = Choices(
    ("male", _("Male")),
    ("female", _("Female")),
    ("other", _("Other")),
)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom users model"""

    # User fields
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        db_index=True,
        unique=True,
    )
    display_name = models.CharField(verbose_name=_("display name"), max_length=100)
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=20,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.male,
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_user,
        validators=[validate_image_size],
        blank=True,
        default="default/profile.jpg",
    )
    country = models.CharField(
        verbose_name=_("country"),
        max_length=200,
        default="UA",
        choices=CountryField().choices + [("", "Select Country")],
    )
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        null=True,
        default="",
        related_name="users",
    )
    type_profile = models.CharField(
        verbose_name=_("type profile"),
        max_length=20,
        choices=TYPE_PROFILE_CHOICES,
        default=TYPE_PROFILE_CHOICES.user,
    )
    is_premium = models.BooleanField(_("is premium"), default=False)
    is_spam_email = models.BooleanField(_("is spam email"), default=False)

    # User permissions
    is_staff = models.BooleanField(_("staff status"), default=False)  # For admin access
    is_active = models.BooleanField(_("active"), default=True)  # For users activation

    # Timestamps
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        """String representation of the user."""
        return self.email

    @property
    def get_profile(self):
        """Returns the profile of the user."""
        if self.has_user_profile():
            return self
        elif self.has_artist_profile():
            return self.artist

    def has_user_profile(self):
        if self.type_profile == TYPE_PROFILE_CHOICES.user:
            return hasattr(self, "user")
        return False

    def has_artist_profile(self):
        if self.type_profile == TYPE_PROFILE_CHOICES.artist:
            return hasattr(self, "artist")
        return False


class Artist(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist")
    first_name = models.CharField(verbose_name=_("first name"), max_length=100)
    last_name = models.CharField(verbose_name=_("last name"), max_length=100)
    display_name = models.CharField(
        verbose_name=_("display name"),
        max_length=100,
        unique=True,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=get_path_upload_image_artist,
        validators=[validate_image_size],
        blank=True,
        default="default/artist.jpg",
    )
    is_verify = models.BooleanField(_("is verify"), default=False)

    class Meta:
        verbose_name = _("artist")
        verbose_name_plural = _("artists")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        """String representation of the artist."""
        return self.display_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
