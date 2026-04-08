"""WSGI config for serving the pensions tracker project."""

import os
from django.core.wsgi import get_wsgi_application
from pensions_tracker.startup import create_superuser


# Create a default superuser if environment variables are set (for development convenience).
create_superuser()

# Ensure Django loads the correct settings module before app startup.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pensions_tracker.settings')
application = get_wsgi_application()
