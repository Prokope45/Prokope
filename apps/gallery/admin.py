"""Gallery admin.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import admin
from apps.gallery.models import (
    CountryAlbum,
    CityGallery,
    CityPhoto,
    City,
    Country
)
from photologue.admin import (
    PhotoAdmin as BasePhotoAdmin
)


class CityGalleryInline(admin.StackedInline):
    model = CityGallery
    extra = 0
    show_change_link = True
    fields = [
        'city', 'date_added', 'is_public', 'city_photos'
    ]
    filter_horizontal = ['city_photos']
    exclude = ('title', 'slug',)


@admin.register(CountryAlbum)
class CountryGalleryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['country']
    inlines = [CityGalleryInline]
    exclude = ('title', 'slug',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """
        Return empty perms dict, hiding the model from admin index.
        """
        return {}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['country']

    def get_model_perms(self, request):
        """
        Return empty perms dict, hiding the model from admin index.
        """
        return {}


@admin.register(CityPhoto)
class CityPhotoAdmin(BasePhotoAdmin):
    autocomplete_fields = ['country', 'city']

    def get_model_perms(self, request):
        """
        Return empty perms dict, hiding the model from admin index.
        """
        return {}
