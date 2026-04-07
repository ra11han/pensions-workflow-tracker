"""ASGI config for serving the pensions tracker project."""

import os
from django.core.asgi import get_asgi_application

# Ensure Django loads the correct settings module before app startup.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pensions_tracker.settings')
application = get_asgi_application()
