"""Gallery view.

Author: Jared Paubel
Version: 0.1
"""
from django.views.generic import ListView, DetailView

from apps.gallery.models import CountryAlbum


class CountryGallery(ListView):
    """Country gallery list view."""

    model = CountryAlbum
    template_name = 'gallery.html'
    queryset = CountryAlbum.objects.all().order_by('country')
    context_object_name = 'gallery_info'


class CountryGalleryDetail(DetailView):
    """Country gallery detail view."""

    model = CountryAlbum
    template_name = 'gallery_detail.html'
