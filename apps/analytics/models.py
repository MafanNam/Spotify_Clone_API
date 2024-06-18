from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.audio.models import Track
from apps.core.models import TimeStampedModel

User = get_user_model()


class Similarity(TimeStampedModel):
    """
    Similarity model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="similarities")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="similarities")
    score = models.DecimalField(_("score"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("similarity")
        verbose_name_plural = _("similarities")
        unique_together = ("user", "track")

    def __str__(self):
        return f"{self.user} - {self.track} - {self.score}"


class TrackPlays(TimeStampedModel):
    """
    Track plays model.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="plays")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="plays")
    viewer_ip = models.GenericIPAddressField(_("viewer IP"), blank=True, null=True)

    class Meta:
        verbose_name = _("track play")
        verbose_name_plural = _("track plays")
        unique_together = ("user", "track", "viewer_ip")

    def __str__(self):
        return f"{self.track.title} listed by {self.user.display_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_listening(cls, track, user, viewer_ip):
        view, _ = cls.objects.get_or_create(track=track, user=user, viewer_ip=viewer_ip)
        view.save()
