"""Gallery models.

Author: Jared Paubel
Version: 0.1
"""
from django.db import models
from photologue.models import Gallery


# Gallery Page
class PhotoGallery(models.Model):
    """Photo gallery model."""

    # TODO: Change format to get Photos directly from Photologue, then generate new
    #   to enforce pagination
    galleries = models.ManyToManyField(Gallery)
    country = models.CharField(max_length=199)
    content = models.TextField()
    slug = models.SlugField(max_length=250, allow_unicode=True, blank=True)

    class Meta:
        ordering = ["country"]
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __str__(self):
        return f"{self.country}"
