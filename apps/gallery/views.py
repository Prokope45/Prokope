"""Gallery view.

Author: Jared Paubel
Version: 0.1
"""
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch

from apps.gallery.models import CountryAlbum, CountryPhoto


class CountryGalleryList(ListView):
    """Country gallery list view."""

    model = CountryAlbum
    template_name = 'gallery.html'
    queryset = CountryAlbum.objects.all().order_by('country')
    context_object_name = 'galleries'


class CountryGalleryDetail(DetailView):
    model = CountryAlbum
    template_name = 'gallery_detail.html'
    context_object_name = 'gallery'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery = self.object
        selected_city = self.request.GET.get('city', 'all')

        # All albums (cities) related to this country
        city_galleries = gallery.city_galleries.select_related(
            'city'
        ).prefetch_related(
            Prefetch('photos', queryset=CountryPhoto.objects.all())
        ).all()

        if selected_city != 'all':
            city_galleries = [
                g for g in city_galleries if g.city.name == selected_city
            ]
        context['city_galleries'] = city_galleries

        # Filtered public photos from this country
        context['country_photos'] = CountryPhoto.objects.filter(
            country=gallery.country,
            is_public=True
        ).select_related('city')

        # List of unique cities as strings
        context['cities'] = list(
            gallery.city_galleries.values_list(
                'city__name', flat=True).distinct()
            )

        context['selected_city'] = selected_city

        for city in context['city_galleries']:
            for photo in city.photos.all():
                print(photo.city)
        return context
