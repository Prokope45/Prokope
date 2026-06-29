from django.utils import timezone
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import OIDCUserProfile


class PocketIDBackend(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super().create_user(claims)
        self.__sync_permissions(user, claims)
        self.__sync_profile(user, claims)
        return user

    def update_user(self, user, claims):
        user = super().update_user(user, claims)
        self.__sync_permissions(user, claims)
        self.__sync_profile(user, claims)
        return user

    def __sync_permissions(self, user, claims):
        groups = claims.get("groups", [])
        user.is_staff = True
        user.is_superuser = "admins" in groups
        user.save()

    def __sync_profile(self, user, claims):
        OIDCUserProfile.objects.update_or_create(
            user=user,
            defaults={
                'sub': claims.get('sub', ''),
                'issuer': claims.get('iss', ''),
                'last_oidc_login': timezone.now(),
            }
        )
