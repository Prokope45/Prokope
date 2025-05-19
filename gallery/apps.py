"""Gallery configs.

Author: Jared Paubel
Version: 0.1
"""
from django.apps import AppConfig


class GalleryConfig(AppConfig):
    """Gallery configuration settings."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'
