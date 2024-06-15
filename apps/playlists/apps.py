from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlaylistsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.playlists"

    verbose_name = _("Playlists")
