"""Blog views tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.models import Tag
from apps.blog.models import Post


class BlogViewTests(TestCase):
    """Blog view tests."""

    def setUp(self):
        """Create clean test data for each test."""
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

        # Create draft (unpublished)
        self.draft = Post.objects.create(
            author=self.user,
            title="Draft Post",
            slug="draft-post",
            content="Hidden post",
            status=0,
        )

        # Ensure tags exist
        self.tag = Tag.objects.get(name="django")

    def test_post_list_view_status_code(self):
        """Test that blog post list is rendered with status 200."""
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_uses_template(self):
        """Test that blog post list uses correct template."""
        response = self.client.get(reverse("blog"))
        self.assertTemplateUsed(response, "blog.html")

    def test_post_list_only_published(self):
        """Test that only published posts are shown."""
        response = self.client.get(reverse("blog"))
        posts = response.context["posts"]
        self.assertEqual(posts.count(), 2)
        self.assertNotIn(self.draft, posts)

    def test_post_list_context_tags(self):
        """Test that context data includes tags."""
        response = self.client.get(reverse("blog"))
        self.assertIn("tag", response.context)

    def test_post_list_sorting(self):
        """Test posts are sorted by date."""
        response = self.client.get(
            reverse("blog") + "?sort=title&order=asc"
        )
        posts = list(response.context["posts"])
        self.assertEqual(posts[0].title, "First Post")
        self.assertEqual(posts[1].title, "Second Post")

    def test_post_list_tag_filtering(self):
        """Test that posts are filtered by tags."""
        response = self.client.get(reverse("blog") + "?tags=django")
        posts = response.context["posts"]
        self.assertEqual(posts.count(), 1)
        self.assertIn(self.post2, posts)
        self.assertNotIn(self.post1, posts)

    def test_post_list_selected_tags_context(self):
        """Test that blogs are shown based on selected tags."""
        response = self.client.get(reverse("blog") + "?tags=django")
        self.assertIn("selected_tags", response.context)
        self.assertEqual(response.context["selected_tags"], ["django"])

    def test_post_detail_view_success(self):
        """Test that post details uses correct template with status 200."""
        response = self.client.get(
            reverse("blog_post", args=[self.post1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog_post.html")
        self.assertEqual(response.context["object"], self.post1)

    def test_post_detail_view_404(self):
        """Test that post detail renders status 404 for invalid post."""
        response = self.client.get(reverse(
            "blog_post", args=["non-existent-slug"])
        )
        self.assertEqual(response.status_code, 404)

    def test_tag_index_view_filters_by_slug(self):
        """Test that index featured blogs filters by tag slug."""
        response = self.client.get(
            reverse("posts_by_tag", args=[self.tag.slug])
        )
        posts = response.context["posts"]
        self.assertEqual(posts.count(), 1)
        self.assertIn(self.post2, posts)

    def test_tag_index_context_has_all_tags(self):
        """Test that index featured blogs has all tags."""
        response = self.client.get(
            reverse("posts_by_tag", args=[self.tag.slug])
        )
        self.assertIn("tag", response.context)
