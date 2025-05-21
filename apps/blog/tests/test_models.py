"""Blog models tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from apps.blog.models import Post


class PostModelTests(TestCase):
    """Blog post model tests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

        self.post = Post.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            author=self.user,
            content="This is the content of the test blog post.",
            status=1,
        )

    def test_post_creation(self):
        """Test that the post is created correctly"""
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, "Test Blog Post")
        self.assertEqual(self.post.status, 1)
        self.assertEqual(self.post.author.username, "testuser")
        self.assertTrue(self.post.created_on)
        self.assertTrue(self.post.updated_on)

    def test_post_str_method(self):
        """Test the string representation of the post"""
        self.assertEqual(str(self.post), "Test Blog Post")

    def test_post_status_choices(self):
        """Test the status field options"""
        draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            author=self.user,
            content="Draft content",
            status=0,
        )
        self.assertEqual(draft_post.status, 0)
        self.assertIn(draft_post.status, dict(Post.STATUS))

    def test_post_ordering(self):
        """Test that posts are ordered by created_on descending"""
        older_post = Post.objects.create(
            title="Older Post",
            slug="older-post",
            author=self.user,
            content="Older content",
            created_on=timezone.now() - timezone.timedelta(days=1),
            status=1
        )

        posts = list(Post.objects.all())
        self.assertEqual(posts[0], self.post) 
        self.assertEqual(posts[1], older_post)

    def test_post_tags(self):
        """Test adding tags to a post"""
        self.post.tag.add("django", "testing")
        self.assertEqual(self.post.tag.count(), 2)
        self.assertIn("django", self.post.tag.names())
