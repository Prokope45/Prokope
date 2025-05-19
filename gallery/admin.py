from django.contrib import admin

from gallery.models import PhotoGallery

class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('country',), }


admin.site.register(PhotoGallery, GalleryAdmin)
