from django.utils.encoding import filepath_to_uri
from photologue.models import PhotoSizeCache
from rest_framework import serializers

from apps.gallery.models import City, CityGallery, CityPhoto, Country, CountryAlbum


def _photo_cache_url(obj, size_name):
    """Build the photologue cache URL deterministically without network I/O.

    Replicates photologue's _get_SIZE_url() path construction but avoids
    size_exists() S3 HEAD requests and increment_count() DB writes,
    since the sizes are pre-generated (PhotoSize.pre_cache=True).
    """
    try:
        photosize = PhotoSizeCache().sizes.get(size_name)
        filename = obj._get_filename_for_size(photosize)
        return '/'.join([obj.cache_url(), filepath_to_uri(filename)])
    except Exception:
        return obj.image.url


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = '__all__'


class CityPhotoSerializer(serializers.ModelSerializer):
    get_display_url = serializers.SerializerMethodField()
    get_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = CityPhoto
        fields = '__all__'

    def get_get_display_url(self, obj):
        return _photo_cache_url(obj, 'display')

    def get_get_thumbnail_url(self, obj):
        return _photo_cache_url(obj, 'thumbnail')


class CityGallerySerializer(serializers.ModelSerializer):
    city = CitySerializer()
    city_photos = CityPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = CityGallery
        fields = ['id', 'title', 'slug', 'city', 'city_photos', 'date_added', 'is_public']


class CountryAlbumListSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    city_galleries = CityGallerySerializer(many=True, read_only=True)

    class Meta:
        model = CountryAlbum
        fields = ['id', 'title', 'slug', 'country', 'city_galleries']


class CountryAlbumDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city_galleries = CityGallerySerializer(many=True, read_only=True)

    class Meta:
        model = CountryAlbum
        fields = '__all__'
