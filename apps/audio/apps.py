from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AudioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audio"

    verbose_name = _("Audio")
