"""App configuration for the accounts module."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Registers metadata for the accounts Django app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
