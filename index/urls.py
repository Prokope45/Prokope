"""Index urls.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path

from index.views import index_view, search

urlpatterns = [
    path('', index_view, name='home'),
    path('search/', search, name='search'),
]
