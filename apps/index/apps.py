"""Index configs.

Author: Jared Paubel
Version: 0.1
"""
from django.apps import AppConfig


class IndexConfig(AppConfig):
    """Index configuration settings."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.index'

    def ready(self):
        import apps.index.signals
