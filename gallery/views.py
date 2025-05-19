"""Gallery view.

Author: Jared Paubel
Version: 0.1
"""
from django.views.generic import ListView, DetailView

from gallery.models import PhotoGallery


class CountryGallery(ListView):
    """Country gallery list view."""

    model = PhotoGallery
    template_name = 'gallery.html'
    queryset = PhotoGallery.objects.all().order_by('country')
    context_object_name = 'gallery_info'


class CountryGalleryDetail(DetailView):
    """Country gallery detail view."""

    model = PhotoGallery
    template_name = 'gallery_detail.html'
