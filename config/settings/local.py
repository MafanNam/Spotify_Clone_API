from .base import *  # noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-a77ec^w-=8mz71we3on8ld&^h46ig$s#+^2c81_^ml3*s*sm38")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=True)

# INSTALLED_APPS += [
#     "debug_toolbar",
# ]

MIDDLEWARE += [
    # TODO: Delete JWTFromCookieMiddleware
    "corsheaders.middleware.CorsMiddleware",
    # "apps.users.middleware.JWTFromCookieMiddleware",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

# EMAIL
# EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = "Spotify Clone <spotify_clone@gmail.com>"

# DEBUG TOOLBAR
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    # "cachalot.panels.CachalotPanel",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: True,
}
