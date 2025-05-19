"""Common test search view.

Author: Jared Paubel
Version: 0.1
"""
from django.core.exceptions import BadRequest, PermissionDenied
from requests import HTTPError
from django.test import TestCase, RequestFactory
from apps.common.views import (
    custom_page_not_found_view, custom_bad_request_view,
    custom_error_view, custom_permission_denied_view
)


class TestSearchView(TestCase):
    """Test common search view."""
    pass
