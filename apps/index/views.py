"""Index view functions.

Author: Jared Paubel
Version: 0.1
"""
from django.shortcuts import render
import random
from django.http import HttpRequest, HttpResponse

from apps.index.models import Index
from apps.blog.models import Post
from apps.gallery.models import CityGallery, CountryAlbum


def index_view(request: HttpRequest) -> HttpResponse:
    """Function-based view that sends index data to template.

    Args:
        request (HttpRequest): Request to process.

    Returns:
        HttpResponse: Response to provide to template.
    """
    context = {
        'index_data': Index.objects.first(),
        'posts': Post.objects.filter(status=1).order_by('-updated_on')[:2],
    }
    if (len(CityGallery.objects.all()) > 0):
        random_gallery = random.choice(CityGallery.objects.all())
        city = random_gallery.city
        context["gallery"] = {
            "country": CountryAlbum.objects.filter(
                city_galleries__city=city
            ).first(),
            "city": city.name,
            "photos": random_gallery.city_photos.all()[:10]
        }
    return render(request, 'index.html', context)
