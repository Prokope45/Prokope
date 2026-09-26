"""Common API tests.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.blog.models import Post
from apps.index.models import Index


class SearchAPITests(TestCase):
    """Search API test class."""

    def setUp(self):
        self.client = APIClient()
        self.index_entry = Index.objects.create(
            about_me_title="My Journey",
            about_me_description="A long story...",
            about_prokope_title="Prokope Origins",
            about_prokope_description="Ancient tales..."
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepass123'
        )

        self.post = Post.objects.create(
            title="Exploring Django",
            content="Django is amazing!",
            author=self.user,
            slug="exploring-django"
        )
        self.post.tag.add("django")

    def test_empty_query_returns_empty_results(self):
        response = self.client.get(reverse('api-search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['about_me'], [])
        self.assertEqual(response.data['blog'], [])
        self.assertEqual(response.data['gallery'], [])

    def test_query_returns_blog_results(self):
        response = self.client.get(
            reverse('api-search'),
            {'q': 'Django'}
        )
        self.assertEqual(response.status_code, 200)
        titles = [p['title'] for p in response.data['blog']]
        self.assertIn('Exploring Django', titles)

    def test_query_returns_index_results(self):
        response = self.client.get(
            reverse('api-search'),
            {'q': 'Journey'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['about_me']), 1)

    def test_sql_injection_returns_error(self):
        response = self.client.get(
            reverse('api-search'),
            {'q': 'SELECT * FROM users;'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.data)
