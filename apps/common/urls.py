"""Common urls.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path

from apps.common.views import search, tailscale_webfinger

urlpatterns = [
    path('search/', search, name='search'),
    path('.well-known/webfinger', tailscale_webfinger, name='tailscale_webfinger')
]
