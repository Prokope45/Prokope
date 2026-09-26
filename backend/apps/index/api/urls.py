from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.index.api.views import IndexViewSet

router = DefaultRouter()
router.register('index', IndexViewSet, basename='index')

urlpatterns = [
    path('', include(router.urls)),
]
