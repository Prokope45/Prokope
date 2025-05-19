"""Blog configs.

Author: Jared Paubel
Version: 0.1
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Blog configuration settings."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
