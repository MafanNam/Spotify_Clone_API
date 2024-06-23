import os

from celery import Celery
from django.conf import settings
from environ import Env

env = Env()

# TODO: change this in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE", default="config.settings.local"))
app = Celery("config")

# Configure Celery using settings from Django base.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# TODO: change this in production
# app.conf.beat_schedule = {
#     "spam-mail-every-week": {
#         "task": "apps.core.tasks.send_spam_email_celery_task",
#         "schedule": crontab(hour="8", minute="0", day_of_week="mon"),
#     }
# }

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
