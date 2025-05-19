from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.urls import path, include

# Force TOTP entry for admin login during production
if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite

handler400 = 'apps.common.views.custom_bad_request_view'
handler403 = 'apps.common.views.custom_permission_denied_view'
handler404 = 'apps.common.views.custom_page_not_found_view'
handler500 = 'apps.common.views.custom_error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.index.urls')),
    path('', include('apps.common.urls')),
    path('blog', include('apps.blog.urls')),
    path('gallery', include('apps.gallery.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
