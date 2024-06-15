from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class SubscriptionPlan(TimeStampedModel):
    """
    Subscription plan model
    """

    name = models.CharField(_("Name"), max_length=100, unique=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    description = models.TextField(_("Description"), blank=True)
    days_exp = models.PositiveIntegerField(_("Days expiration"), default=0)
    feature = models.ManyToManyField(
        "Feature",
        blank=True,
        related_name="subscription_plan",
    )

    class Meta:
        verbose_name = _("Subscription plan")
        verbose_name_plural = _("Subscription plans")

    def __str__(self):
        return self.name


class Feature(TimeStampedModel):
    """
    Feature model
    """

    name = models.CharField(_("Name"), max_length=255)
    permission = models.CharField(_("Permission"), max_length=255)

    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")

    def __str__(self):
        return self.name
