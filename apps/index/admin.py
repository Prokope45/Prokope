"""Index admin.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import admin

from apps.index.models import Index


class IndexAdmin(admin.ModelAdmin):
    """Index admin settings."""

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
