"""Blog API tests.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.blog.models import Post


class BlogPostAPITests(TestCase):
    """Blog post API test class."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

        self.post1 = Post.objects.create(
            author=self.user,
            title="First Post",
            slug="first-post",
            content="Hello world",
            status=1,
        )
        self.post2 = Post.objects.create(
            author=self.user,
            title="Second Post",
            slug="second-post",
            content="Another post",
            status=1,
        )
        self.post2.tag.add("django")

        self.draft = Post.objects.create(
            author=self.user,
            title="Draft Post",
            slug="draft-post",
            content="Hidden post",
            status=0,
        )

    def test_post_list_returns_200(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_only_published(self):
        response = self.client.get(reverse('post-list'))
        slugs = [p['slug'] for p in response.data['results']]
        self.assertIn('first-post', slugs)
        self.assertIn('second-post', slugs)
        self.assertNotIn('draft-post', slugs)

    def test_post_list_paginated(self):
        response = self.client.get(reverse('post-list'))
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_post_detail_returns_200(self):
        response = self.client.get(
            reverse('post-detail', args=[self.post1.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_returns_full_content(self):
        response = self.client.get(
            reverse('post-detail', args=[self.post1.slug])
        )
        self.assertEqual(response.data['title'], 'First Post')
        self.assertIn('content', response.data)
        self.assertIn('tag', response.data)

    def test_post_detail_404(self):
        response = self.client.get(
            reverse('post-detail', args=['non-existent-slug'])
        )
        self.assertEqual(response.status_code, 404)

    def test_post_list_filter_by_tag(self):
        response = self.client.get(
            reverse('post-list'),
            {'tags': 'django'}
        )
        slugs = [p['slug'] for p in response.data['results']]
        self.assertEqual(len(slugs), 1)
        self.assertIn('second-post', slugs)

    def test_tag_list_returns_200(self):
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, 200)

    def test_tag_list_contains_tags(self):
        response = self.client.get(reverse('tag-list'))
        names = [t['name'] for t in response.data]
        self.assertIn('django', names)

    def test_contact_create_unauthenticated(self):
        response = self.client.post(reverse('contact-create'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Hello',
            'message': 'Test message',
        })
        self.assertEqual(response.status_code, 201)
