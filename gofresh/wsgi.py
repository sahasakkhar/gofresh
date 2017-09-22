"""
WSGI config for gogresh project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from gofresh.settings import DEBUG
from django.core.wsgi import get_wsgi_application


if DEBUG is True:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gofresh.local_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gofresh.aws_settings")

application = get_wsgi_application()
