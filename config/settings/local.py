from .base import *  # noqa
from .base import env


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default='django-insecure-a77ec^w-=8mz71we3on8ld&^h46ig$s#+^2c81_^ml3*s*sm38')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=True)
