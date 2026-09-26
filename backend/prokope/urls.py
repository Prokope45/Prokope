from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path('', include('api.urls')),
    path('', include('apps.common.urls')),
    path('blog/', include('apps.blog.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)