from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.urls import path, include
from django.conf.urls import (
    handler400, handler404, handler500
)

# Force TOTP entry for admin login during production
if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite

handler404 = 'blog.views.custom_page_not_found_view'
handler500 = 'blog.views.custom_error_view'
handler400 = 'blog.views.custom_bad_request_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
