from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.gallery.api.views import (
    CityPhotoViewSet,
    CityViewSet,
    CountryAlbumViewSet,
    CountryViewSet,
)

router = DefaultRouter()
router.register('countries', CountryViewSet, basename='country')
router.register('cities', CityViewSet, basename='city')
router.register('photos', CityPhotoViewSet, basename='photo')
router.register('country-albums', CountryAlbumViewSet, basename='country-album')

urlpatterns = [
    path('', include(router.urls)),
]
