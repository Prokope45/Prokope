"""Index models.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import admin

from index.models import Index


class IndexAdmin(admin.ModelAdmin):
    """Index admin settings."""

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
        """Remove delete permissions."""
        return True

    def has_add_permission(self, request):
        """Remove add permissions."""
        return False

    def has_change_permission(self, request, obj=Index.greeting_title):
        """Allow edit permissions."""
        return True


admin.site.register(Index, IndexAdmin)
