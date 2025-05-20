"""Common urls.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path

from apps.common.views import search

urlpatterns = [
    path('search/', search, name='search'),
]
