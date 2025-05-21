"""Blog admin.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from apps.blog.models import Post, Contact


class PostAdmin(SummernoteModelAdmin):
    """Blog post admin settings."""

    summernote_fields = ('content',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
# admin.site.register(Contact)
