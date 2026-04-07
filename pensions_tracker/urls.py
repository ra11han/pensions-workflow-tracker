"""Root URL configuration for the pensions tracker project."""

from django.contrib import admin
from django.urls import path, include

# Mounts admin, auth, account management, and tracker feature routes.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('tracker.urls')),
]
