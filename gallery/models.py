from django.db import models
from photologue.models import Gallery


# Gallery Page
# TODO: Change format to get Photos directly from Photologue, then generate new
#   to enforce pagination
class PhotoGallery(models.Model):
    galleries = models.ManyToManyField(Gallery)
    country = models.CharField(max_length=199)
    content = models.TextField()
    slug = models.SlugField(max_length=250, allow_unicode=True, blank=True)

    class Meta:
        ordering = ["country"]

    def __str__(self):
        return f"{self.country}"
