import os
from celery import Celery
from datetime import timedelta
from gofresh.settings import DEBUG

if DEBUG is True:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gofresh.local_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gofresh.aws_settings")

app = Celery('gofresh')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.timezone = 'UTC'
