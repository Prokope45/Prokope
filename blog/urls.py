from . import views
from django.urls import path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import index_view, search

urlpatterns = [
    path('', index_view, name='home'),
    path('update_server/', views.update, name='update'),
    path('blog/', views.PostList.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('gallery/', views.Gallery.as_view(), name='gallery'),
    path('gallery/<slug:slug>/', views.GalleryDetail.as_view(), name='gallery_detail'),
    path('tags/<slug:tag_slug>/', views.TagIndexView.as_view(), name='posts_by_tag'),
    path('search/', search, name='search'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
]
