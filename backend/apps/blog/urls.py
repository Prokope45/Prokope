"""Blog urls.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path

from apps.blog.views import update

urlpatterns = [
    path('update_server/', update, name='update'),
]