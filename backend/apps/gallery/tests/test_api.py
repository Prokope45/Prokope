"""Gallery API tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.gallery.models import City, CityGallery, CityPhoto, Country, CountryAlbum


class GalleryAPITests(TestCase):
    """Gallery API test class."""

    def setUp(self):
        self.client = APIClient()

        self.france = Country.objects.create(name="France")
        self.album = CountryAlbum.objects.create(
            country=self.france,
        )
        self.paris = City.objects.create(
            name="Paris",
            country=self.france
        )
        self.city_gallery = CityGallery.objects.create(
            album=self.album,
            city=self.paris
        )

    def test_country_list_returns_200(self):
        response = self.client.get(reverse('country-list'))
        self.assertEqual(response.status_code, 200)

    def test_country_list_contains_countries(self):
        response = self.client.get(reverse('country-list'))
        names = [c['name'] for c in response.data['results']]
        self.assertIn('France', names)

    def test_city_list_returns_200(self):
        response = self.client.get(reverse('city-list'))
        self.assertEqual(response.status_code, 200)

    def test_city_list_filter_by_country(self):
        response = self.client.get(
            reverse('city-list'),
            {'country': self.france.pk}
        )
        names = [c['name'] for c in response.data['results']]
        self.assertIn('Paris', names)

    def test_country_album_list_returns_200(self):
        response = self.client.get(reverse('country-album-list'))
        self.assertEqual(response.status_code, 200)

    def test_country_album_detail_returns_200(self):
        response = self.client.get(
            reverse('country-album-detail', args=[self.album.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_country_album_detail_contains_city_galleries(self):
        response = self.client.get(
            reverse('country-album-detail', args=[self.album.slug])
        )
        self.assertIn('city_galleries', response.data)
        self.assertEqual(len(response.data['city_galleries']), 1)

    def test_photo_list_returns_200(self):
        response = self.client.get(reverse('photo-list'))
        self.assertEqual(response.status_code, 200)
