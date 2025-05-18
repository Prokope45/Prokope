from django.contrib import admin
from django.conf import settings
from django_summernote.admin import SummernoteModelAdmin

from .models import Index, Post, Contact, PhotoGallery


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    prepopulated_fields = { 'slug': ('title',), }


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('country',), }


class IndexAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        """Construct IndexAdmin object."""
        super().__init__(model, admin_site)
        self.__autocreate_index_object()

    def __autocreate_index_object(self):
        """Auto-create index object if it does not already exist."""
        obj, was_created = Index.objects.get_or_create(
            greeting_title='Welcome to Prokope.io!'
        )
        if not was_created:
            obj.save()

    def has_delete_permission(self, request, obj=Index.greeting_title):
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=Index.greeting_title):
        return True


admin.site.register(Index, IndexAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PhotoGallery, GalleryAdmin)
admin.site.register(Contact)
