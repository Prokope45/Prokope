"""Gallery admin.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path
from django.shortcuts import render
from django.contrib import helpers
from photologue.forms import UploadZipForm
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
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

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict, hiding the model from admin index.
    #     """
    #     return {}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload_zip/',
                 self.admin_site.admin_view(self.upload_zip),
                 name='photologue_upload_zip')
        ]
        return custom_urls + urls

    def upload_zip(self, request):
        context = {
            'title': _('Upload a zip archive of photos'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(form,
                                                 list([(None, {'fields': form.base_fields})]),
                                                 {})
        return render(request, 'admin/photologue/photo/upload_zip.html', context)
