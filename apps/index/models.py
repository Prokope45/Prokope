"""Index models.

Author: Jared Paubel
Version: 0.1
"""
from django.db import models


class Index(models.Model):
    """Index model."""

    hero_banner = models.ImageField(
        upload_to="images",
        default="/images/default/default_hero_banner.png"
    )
    hero_image = models.ImageField(
        upload_to="images",
        default="/images/default/default_hero_image.png"
    )

    greeting_title = models.CharField(
        max_length=200,
        default='Welcome to Prokope.io!',
        null=True
    )
    greeting_description = models.TextField(
        default='My personal portfolio for my thoughts and achievements.',
        null=True
    )

    about_me_title = models.CharField(
        max_length=200,
        default='About Jay',
        null=True
    )
    about_me_description = models.TextField(
        default=(
            "I\'m from Kansas, served in the Marines, and work as a software ",
            "developer intern while studying at Kansas State University"
        ),
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
