from django.urls import path
from gallery.views import CountryGallery, CountryGalleryDetail


urlpatterns = [
    path('', CountryGallery.as_view(), name='gallery'),
    path('<slug:slug>/', CountryGalleryDetail.as_view(), name='gallery_detail'),
]
