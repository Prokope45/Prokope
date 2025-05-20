"""Blog Forms.

Author: Jared Paubel
Version: 0.1
"""
from django import forms
from django.conf import settings
import requests
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from apps.blog.models import Contact


def validate_captcha(value):
    """Verify captcha result."""
    data = {'secret': settings.HCAPTCHA_SECRET, 'response': value}
    response = requests.post(settings.VERIFY_URL, data)
    if 'success' not in response.json() or not response.json()['success']:
        raise ValidationError('hcaptcha is not correct')


class ContactForm(ModelForm):
    """Contact form."""

    captcha = forms.CharField(max_length=10000, validators=[validate_captcha])

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': '',
            'email': '',
            'subject': '',
            'message': '',
        }
