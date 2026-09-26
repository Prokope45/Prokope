"""Gallery admin.

Author: Jared Paubel
Version: 0.1
"""
from io import BytesIO
from zipfile import ZipFile

from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from photologue.admin import PhotoAdmin
from photologue.forms import UploadZipForm

from apps.gallery.models import City, CityGallery, CityPhoto, Country, CountryAlbum


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


class CityPhotoZipUploadForm(UploadZipForm):
    """Form for uploading a zip file as CityPhoto objects."""
    gallery = forms.ModelChoiceField(
        queryset=CityGallery.objects.select_related('city', 'album__country').all(),
        label=_("City Gallery"),
        required=True
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=_("City"),
        required=False
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label=_("Country"),
        required=False
    )


@admin.register(CityPhoto)
class CityPhotoAdmin(PhotoAdmin):
    autocomplete_fields = ['country', 'city']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'upload_zip/',
                self.admin_site.admin_view(self.upload_zip),
                name='gallery_cityphoto_upload_zip',
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['upload_zip_url'] = reverse(
            'admin:gallery_cityphoto_upload_zip'
        )
        return super().changelist_view(request, extra_context=extra_context)

    def upload_zip(self, request):
        opts = self.model._meta
        app_label = opts.app_label

        if request.method == 'POST':
            form = CityPhotoZipUploadForm(request.POST, request.FILES)
            if form.is_valid():
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                zip_file = request.FILES['zip_file']
                with ZipFile(zip_file) as archive:
                    for idx, filename in enumerate(
                        archive.namelist(),
                        start=1
                    ):
                        if (
                            filename.startswith('__MACOSX/') or  # MacOS resource fork junk
                            filename.startswith('.') or  # hidden files like .DS_Store
                            filename.endswith('/')  # directories inside the ZIP
                        ):
                            continue

                        if filename.lower().endswith(
                            ('.jpg', '.jpeg', '.png', '.gif')
                        ):
                            data = archive.read(filename)
                            photo = CityPhoto()
                            photo.title = f"{city.name} {idx}"
                            photo.slug = self.generate_unique_slug(
                                CityPhoto, city
                            )
                            photo.image.save(filename, BytesIO(data))
                            photo.city = city
                            photo.country = country
                            photo.save()
                messages.success(request, _("Photos uploaded successfully."))
                return redirect('admin:gallery_cityphoto_changelist')
        else:
            form = CityPhotoZipUploadForm()

        context = {
            'form': form,
            'opts': opts,
            'app_label': app_label,
            'has_change_permission': self.has_change_permission(request),
        }
        return render(request, 'admin/gallery/upload_zip.html', context)

    def generate_unique_slug(self, model, base_text):
        slug_base = slugify(base_text) or 'photo'
        slug = slug_base
        counter = 1
        while model.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{counter}"
            counter += 1
        return slug

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict, hiding the model from admin index.
    #     """
    #     return {}
