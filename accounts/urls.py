"""URL routes for account registration flows."""

from django.urls import path
from . import views

# Exposes the registration endpoint used alongside Django auth URLs.
urlpatterns = [
    path('register/', views.register, name='register'),
]
