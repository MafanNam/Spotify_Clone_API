from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArtistsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.artists"
    verbose_name = _("Artists")
