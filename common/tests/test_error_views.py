"""Common test error views.

Author: Jared Paubel
Version: 0.1
"""
from django.core.exceptions import BadRequest, PermissionDenied
from requests import HTTPError
from django.test import TestCase, RequestFactory
from common.views import (
    custom_page_not_found_view, custom_bad_request_view,
    custom_error_view, custom_permission_denied_view
)


class TestErrorViews(TestCase):
    """Test common views."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_custom_bad_request_view(self):
        """Simulate a bad request."""
        request = self.factory.get('/bad-request/')

        with self.assertRaises(BadRequest):
            raise BadRequest

        response = custom_bad_request_view(request)
        self.assertContains(
            response,
            text="<title>Prokope | Unexpected Problem</title>",
            status_code=400
        )

    def test_custom_page_not_found_view(self):
        """Simulate a request for a page that doesn't exist."""
        request = self.factory.get('/nonexistent-page/')
        response = custom_page_not_found_view(request)
        self.assertContains(
            response,
            text="<title>Prokope | Nonexistent Page</title>",
            status_code=404
        )

    def test_custom_error_view(self):
        """Simulate a server error."""
        with self.assertRaises(HTTPError):
            raise HTTPError

        request = self.factory.get('/cause-500-error/')
        response = custom_error_view(request)
        self.assertContains(
            response,
            text="<title>Prokope | Server Issue</title>",
            status_code=500
        )

    def test_custom_permission_denied_view(self):
        """Simulate a permission denied error."""
        with self.assertRaises(PermissionDenied):
            raise PermissionDenied

        request = self.factory.get('/not-allowed/')
        response = custom_permission_denied_view(request)

        self.assertContains(
            response,
            text="<title>Prokope | Permission Denied</title>",
            status_code=403
        )
