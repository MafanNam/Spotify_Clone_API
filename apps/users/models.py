from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from model_utils import Choices

from apps.core.services import get_path_upload_image_user, validate_image_size

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
    country = CountryField(
        verbose_name=_("country"),
        blank_label="Select Country",
        default="UA",
    )
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default="",
        related_name="users",
    )
    type_profile = models.CharField(
        verbose_name=_("type profile"),
        max_length=20,
        choices=TYPE_PROFILE_CHOICES,
        default=TYPE_PROFILE_CHOICES.user,
    )
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)
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
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """String representation of the user."""
        return self.email

    def save(self, *args, **kwargs):
        email_username, _ = self.email.split("@", 1)
        if self.display_name == "" or self.display_name is None:
            self.display_name = email_username
        super(User, self).save(*args, **kwargs)

    @property
    def get_profile(self):
        """Returns the profile of the user."""
        if self.has_user_profile():
            return self
        elif self.has_artist_profile():
            return self.artist

    def has_user_profile(self):
        return self.type_profile == TYPE_PROFILE_CHOICES.user

    def has_artist_profile(self):
        return self.type_profile == TYPE_PROFILE_CHOICES.artist

    def follow(self, user):
        self.followers.add(user)

    def unfollow(self, user):
        self.followers.remove(user)

    def check_following(self, user_id):
        return self.followers.filter(id=user_id).exists()

    @property
    def follower_count(self):
        return self.followers.count()
