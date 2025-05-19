"""Index model tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from index.models import Index


class IndexModelTest(TestCase):
    """Index model test class."""

    def setUp(self):
        """Create clean test data for each test."""
        self.__index = Index.objects.create()

    def test_default_hero_banner(self):
        self.assertEqual(
            self.__index.hero_banner.name,
            "/images/default/default_hero_banner.png"
        )

    def test_set_hero_banner(self):
        index = Index.objects.create(
            hero_banner="/images/default/some_other_image.png"
        )
        self.assertEqual(
            index.hero_banner.name,
            "/images/default/some_other_image.png"
        )

    def test_default_hero_image(self):
        self.assertEqual(
            self.__index.hero_image.name,
            "/images/default/default_hero_image.png"
        )

    def test_set_hero_image(self):
        index = Index.objects.create(
            hero_image="/images/default/some_other_image.png"
        )
        self.assertEqual(
            index.hero_image.name,
            "/images/default/some_other_image.png"
        )

    def test_default_greeting_title(self):
        self.assertEqual(
            self.__index.greeting_title,
            "Welcome to Prokope.io!"
        )

    def test_default_greeting_description(self):
        self.assertEqual(
            self.__index.greeting_description,
            "My personal portfolio for my thoughts and achievements."
        )

    def test_custom_greeting_values(self):
        index = Index.objects.create(
            greeting_title="Hi there!",
            greeting_description="Custom description."
        )
        self.assertEqual(index.greeting_title, "Hi there!")
        self.assertEqual(index.greeting_description, "Custom description.")

    def test_default_about_me_title(self):
        self.assertEqual(
            self.__index.about_me_title,
            "About Jay"
        )

    def test_default_about_me_description(self):
        self.assertEqual(
            self.__index.about_me_description,
            ("I\'m from Kansas, served in the Marines, and work as a software ",
             "developer intern while studying at Kansas State University")
        )

    def test_custom_about_me_values(self):
        index = Index.objects.create(
            about_me_title="About Me",
            about_me_description="Something about me."
        )
        self.assertEqual(index.about_me_title, "About Me")
        self.assertEqual(index.about_me_description, "Something about me.")

    def test_default_about_prokope_title(self):
        self.assertEqual(
            self.__index.about_prokope_title,
            "What is 'Prokope'"
        )

    def test_default_about_prokope_description(self):
        self.assertEqual(
            self.__index.about_prokope_description,
            "Prokope means 'to chop down what gets in the way'"
        )

    def test_custom_about_prokope_values(self):
        index = Index.objects.create(
            about_prokope_title="About some other site",
            about_prokope_description="A description about some other site."
        )
        self.assertEqual(index.about_prokope_title, "About some other site")
        self.assertEqual(
            index.about_prokope_description,
            "A description about some other site."
        )

    def test_model_name(self):
        self.assertEqual(
            str(self.__index),
            "Greeting, About Me & Prokope.io"
        )
