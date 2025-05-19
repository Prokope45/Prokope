"""Blog urls.

Author: Jared Paubel
Version: 0.1
"""
from blog.views import update, PostList, PostDetail, TagIndexView
from django.urls import path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('update_server/', update, name='update'),
    path('', PostList.as_view(), name='blog'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('tags/<slug:tag_slug>/', TagIndexView.as_view(), name='posts_by_tag'),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon/favicon.ico'))
    ),
]
