from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from shortuuidfield import ShortUUIDField

from apps.core.models import TimeStampedModel

User = get_user_model()

METHOD_CHOICES = Choices(
    ("paypal", _("PayPal")),
    ("stripe", _("Stripe")),
)

STATUS_CHOICES = Choices(
    ("pending", _("Pending")),
    ("success", _("Success")),
    ("failed", _("Failed")),
    ("canceled", _("Canceled")),
    ("refunded", _("Refunded")),
)


class Payment(TimeStampedModel):
    """
    Payment model.
    """

    payment_id = ShortUUIDField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(
        _("Payment Method"),
        max_length=50,
        choices=METHOD_CHOICES,
        default=METHOD_CHOICES.paypal,
    )
    status = models.CharField(
        _("Payment Status"),
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.pending,
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, default=0)
    tax = models.ForeignKey("Tax", on_delete=models.SET_NULL, null=True, related_name="payments")
    total_price = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"{self.user} - {self.status}"

    def save(self, *args, **kwargs):
        self.total_price = self.price + self.tax.value
        super(Payment, self).save(*args, **kwargs)


class Tax(TimeStampedModel):
    """
    Tax model.
    """

    name = models.CharField(_("Tax Name"), max_length=255)
    value = models.DecimalField(_("Tax"), max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Tax")
        verbose_name_plural = _("Taxes")

    def __str__(self):
        return f"{self.name} - {self.value}"
