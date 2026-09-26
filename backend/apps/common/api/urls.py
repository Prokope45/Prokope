from django.urls import path

from apps.common.api.views import SearchAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='api-search'),
]
