from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.gallery.api.serializers import (
    CityPhotoSerializer,
    CitySerializer,
    CountryAlbumDetailSerializer,
    CountryAlbumListSerializer,
    CountrySerializer,
)
from apps.gallery.models import City, CityGallery, CityPhoto, Country, CountryAlbum


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = []


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']


class CityPhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CityPhoto.objects.all()
    serializer_class = CityPhotoSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'country']


class CountryAlbumViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    permission_classes = []

    def get_queryset(self):
        qs = CountryAlbum.objects.all().order_by('country')
        if self.action == 'list':
            qs = qs.prefetch_related(
                Prefetch(
                    'city_galleries',
                    queryset=CityGallery.objects.filter(
                        city_photos__isnull=False
                    ).distinct()
                )
            )
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CountryAlbumListSerializer
        return CountryAlbumDetailSerializer
