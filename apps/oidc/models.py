from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class OIDCUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oidc_profile')
    sub = models.CharField(max_length=255, unique=True)  # OIDC subject identifier
    last_oidc_login = models.DateTimeField(auto_now=True)
    issuer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} (OIDC)"
