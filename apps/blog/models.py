"""Blog models.

Author: Jared Paubel
Version: 0.1
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from taggit.managers import TaggableManager


# Blog Page
class Post(models.Model):
    """Blog post model."""

    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    updated_on = models.DateField(default=timezone.now)
    created_on = models.DateField(default=timezone.now)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    thumb = models.ImageField(blank=True)
    tag = TaggableManager()

    class Meta:
        """Meta class for blog post."""

        ordering = ['-created_on']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        """String magic method for the class name."""
        return self.title


# Contact Page
class Contact(models.Model):
    """Blog contact model."""

    name = models.CharField(max_length=255, default='')
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        """String magic method for the class name."""
        return self.email
