"""Gallery view.

Author: Jared Paubel
Version: 0.1
"""
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch

from apps.gallery.models import CountryAlbum, CityPhoto, CityGallery


class CountryGalleryList(ListView):
    """Country gallery list view."""

    model = CountryAlbum
    template_name = 'gallery.html'

    # Filter out galleries with no city photos.
    albums = CountryAlbum.objects.prefetch_related(
        Prefetch(
            'city_galleries',
            queryset=CityGallery.objects.filter(
                city_photos__isnull=False
            ).distinct()
        )
    )

    queryset = albums.all().order_by('country')
    context_object_name = 'albums'


class CountryGalleryDetail(DetailView):
    model = CountryAlbum
    template_name = 'gallery_detail.html'
    context_object_name = 'gallery'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery = self.object
        selected_city = self.request.GET.get('city', 'all')

        # All albums (cities) related to this country as CountryPhoto objs
        city_galleries = gallery.city_galleries.select_related(
            'city'
        ).prefetch_related(
            Prefetch('photos', queryset=CityPhoto.objects.all())
        ).all()

        # Get photos for selected city
        if selected_city != 'all':
            city_galleries = [
                g for g in city_galleries if g.city.name == selected_city
            ]
        context['city_galleries'] = city_galleries

        # List of unique cities as strings to populate select field
        context['cities'] = list(
            gallery.city_galleries.values_list(
                'city__name', flat=True).distinct()
            )
        context['selected_city'] = selected_city

        return context
