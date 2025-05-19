"""Gallery admin.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import admin

from gallery.models import PhotoGallery


class GalleryAdmin(admin.ModelAdmin):
    """Gallery admin settings."""

    prepopulated_fields = {'slug': ('country',)}


admin.site.register(PhotoGallery, GalleryAdmin)
