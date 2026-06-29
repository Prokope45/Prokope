from django.contrib import admin
from django.contrib.auth import get_user_model
from django_otp.admin import OTPAdminSite
from .models import OIDCUserProfile

User = get_user_model()


class HybridAdminSite(OTPAdminSite):

    def has_permission(self, request):

        # Allow access if authenticated via OIDC (no OTP required)
        if (
            request.user.is_active
            and request.user.is_staff
            and not request.user.is_anonymous
        ):
            return request.user.is_staff
        return super().has_permission(request)


@admin.register(OIDCUserProfile)
class OIDCUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'sub', 'issuer', 'last_oidc_login']
    readonly_fields = ['user', 'sub', 'issuer', 'last_oidc_login']
