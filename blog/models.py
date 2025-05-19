from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from taggit.managers import TaggableManager

from photologue.models import Gallery, Photo


# Blog Page
class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateField(default=timezone.now)
    created_on = models.DateField(default=timezone.now)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    thumb = models.ImageField(blank=True)
    tag = TaggableManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


# Gallery Page
# TODO: Change format to get Photos directly from Photologue, then generate new
#   to enforce pagination
class PhotoGallery(models.Model):
    galleries = models.ManyToManyField(Gallery)
    country = models.CharField(max_length=199)
    content = models.TextField()
    slug = models.SlugField(max_length=250, allow_unicode=True, blank=True)

    class Meta:
        ordering = ["country"]

    def __str__(self):
        return f"{self.country}"


# Contact Page
class Contact(models.Model):
    name = models.CharField(max_length=255, default='')
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email
