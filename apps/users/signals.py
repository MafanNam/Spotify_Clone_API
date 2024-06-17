from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.artists.models import Artist

from .models import TYPE_PROFILE_CHOICES

User = get_user_model()


@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    """Create a user artist profile when a new user is created."""
    if not instance.is_superuser:
        if created and not kwargs.get("raw", False):
            if instance.type_profile == TYPE_PROFILE_CHOICES.artist:
                Artist.objects.create(
                    user=instance,
                    display_name=instance.display_name,
                    image=instance.image,
                )


@receiver(post_save, sender=User)
def save_artist_profile(sender, instance, **kwargs):
    """Save the user artist profile when the user is saved."""
    if not instance.is_superuser and not kwargs.get("raw", False):
        if instance.type_profile == TYPE_PROFILE_CHOICES.artist:
            instance.artist.save()
