from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from taggit.managers import TaggableManager

from photologue.models import Gallery, Photo


# Index Page
class Index(models.Model):
    hero_banner = models.ImageField(
        upload_to="images",
        default="/images/default/default_hero_banner.png"
    )
    hero_image = models.ImageField(
        upload_to="images",
        default="/images/default/default_hero_image.png"
    )

    greeting_title = models.CharField(max_length=200, default='Welcome to Prokope.io!', null=True)
    greeting_description = models.TextField(
        default='My personal portfolio for my thoughts and achievements.',
        null=True
    )

    about_me_title = models.CharField(max_length=200, default='About Jay', null=True)
    about_me_description = models.TextField(
        default='I\'m from Kansas, served in the Marines, and work as a software developer intern while studying at Kansas State University',
        null=True
    )

    about_prokope_title = models.CharField(
        max_length=200,
        default="What is 'Prokope'",
        null=True
    )
    about_prokope_description = models.TextField(
        default="Prokope means 'to chop down what gets in the way'",
        null=True
    )

    def __str__(self):
        return "Greeting, About Me & Prokope.io"

    class Meta:
        verbose_name = "Index"
        verbose_name_plural = "Index"

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
