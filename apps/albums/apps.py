from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AlbumsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.albums"

    verbose_name = _("Albums")
