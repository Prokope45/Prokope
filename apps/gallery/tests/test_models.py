"""Gallery models tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from photologue.models import Gallery as PhotoLogueGallery
from apps.gallery.models import PhotoGallery


class PhotoGalleryModelTests(TestCase):
    """Photo gallery model tests."""

    def setUp(self):
        """Create clean test data for each test."""
        self.gallery1 = PhotoLogueGallery.objects.create(
            title="Nature",
            slug="nature"
        )
        self.gallery2 = PhotoLogueGallery.objects.create(
            title="Urban",
            slug="urban"
        )

    def test_create_photogallery(self):
        """Test creation of new country gallery."""
        pg = PhotoGallery.objects.create(
            country="France",
            content="A beautiful photo collection from France.",
            slug="france-gallery"
        )
        pg.galleries.set([self.gallery1, self.gallery2])
        pg.save()

        self.assertEqual(pg.country, "France")
        self.assertEqual(pg.slug, "france-gallery")
        self.assertEqual(
            pg.content,
            "A beautiful photo collection from France."
        )
        self.assertEqual(pg.galleries.count(), 2)

    def test_model_name(self):
        """Test model name."""
        pg = PhotoGallery.objects.create(
            country="Japan",
            content="Japanese collection"
        )
        self.assertEqual(str(pg), "Japan")

    def test_ordering_by_country(self):
        """Test ordering of galleries by country."""
        PhotoGallery.objects.create(
            country="Brazil",
            content="Photos from Brazil"
        )
        PhotoGallery.objects.create(
            country="Argentina",
            content="Photos from Argentina"
        )
        PhotoGallery.objects.create(
            country="Canada",
            content="Photos from Canada"
        )

        countries = list(PhotoGallery.objects.values_list(
            "country", flat=True
        ))
        self.assertEqual(countries, ["Argentina", "Brazil", "Canada"])

    def test_slug_blank(self):
        """Test that slug is blank if not specified."""
        pg = PhotoGallery.objects.create(
            country="Italy",
            content="Italian gallery"
        )
        self.assertEqual(pg.slug, "")
