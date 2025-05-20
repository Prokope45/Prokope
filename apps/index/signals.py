"""Index signals.

Author: Jared Paubel
Version: 0.1
"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.index.models import Index


@receiver(post_migrate)
def create_index_object(sender, **kwargs):
    """Create index object only once after migrations are run."""
    if sender.name == 'apps.index':
        obj, created = Index.objects.get_or_create()
        if not created:
            obj.save()
