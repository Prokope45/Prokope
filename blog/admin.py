from django.contrib import admin
from django.conf import settings
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Contact, PhotoGallery


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    prepopulated_fields = { 'slug': ('title',), }


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('country',), }


admin.site.register(Post, PostAdmin)
admin.site.register(PhotoGallery, GalleryAdmin)
admin.site.register(Contact)
