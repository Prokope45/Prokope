from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Contact


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    prepopulated_fields = { 'slug': ('title',), }


admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
