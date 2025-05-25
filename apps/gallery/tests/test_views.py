"""Gallery views tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from django.urls import reverse
from apps.gallery.models import PhotoGallery


class CountryGalleryViewTests(TestCase):
    """Test country gallery list view."""

    def setUp(self):
        """Create clean test data for each test."""
        self.gallery1 = PhotoGallery.objects.create(
            country="Japan",
            content="Photos from Japan",
            slug="japan"
        )
        self.gallery2 = PhotoGallery.objects.create(
            country="Brazil",
            content="Photos from Brazil",
            slug="brazil"
        )

    def test_list_view_status_code(self):
        """Test that endpoint is reached with status 200."""
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_template(self):
        """Test that endpoint uses correct template."""
        response = self.client.get(reverse("gallery"))
        self.assertTemplateUsed(response, "gallery.html")

    def test_list_view_context(self):
        """Test that context data is expected."""
        response = self.client.get(reverse("gallery"))
        self.assertIn("gallery_info", response.context)
        countries = list(
            response.context["gallery_info"].values_list("country", flat=True)
        )
        self.assertEqual(countries, ["Brazil", "Japan"])


class CountryGalleryDetailViewTests(TestCase):
    """Test country gallery detail view."""

    def setUp(self):
        """Create clean test data for each test."""
        self.gallery = PhotoGallery.objects.create(
            country="France",
            content="Photos from France",
            slug="france"
        )

    def test_detail_view_status_code(self):
        """Test that endpoint is reached with status 200."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.gallery.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_template(self):
        """Test that endpoint uses correct template."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.gallery.slug])
        )
        self.assertTemplateUsed(response, "gallery_detail.html")

    def test_detail_view_context(self):
        """Test that context data is expected."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.gallery.slug])
        )
        self.assertEqual(response.context["object"], self.gallery)

    def test_detail_view_404(self):
        """Test that endpoint displays 404 for invalid detail view."""
        response = self.client.get(
            reverse("gallery_detail", args=["non-existent-slug"])
        )
        self.assertEqual(response.status_code, 404)
