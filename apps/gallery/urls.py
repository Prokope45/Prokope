"""Gallery urls.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path
from apps.gallery.views import CountryGallery, CountryGalleryDetail


urlpatterns = [
    path('', CountryGallery.as_view(), name='gallery'),
    path('<slug:slug>/', CountryGalleryDetail.as_view(), name='gallery_detail'),
]
