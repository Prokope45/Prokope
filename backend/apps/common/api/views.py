import re

from django.conf import settings
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import TaggedItem

from apps.blog.models import Post
from apps.common.api.serializers import (
    BlogSearchSerializer,
    GallerySearchSerializer,
    IndexSearchSerializer,
)
from apps.gallery.models import CountryAlbum
from apps.index.models import Index


class EnvironmentAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        env = settings.ENVIRONMENT
        db_labels = {
            'production': 'Production DB',
            'QA': 'Prod Copy DB',
            'development': 'Test DB',
        }
        return Response({
            'environment': env,
            'database_label': db_labels.get(env, 'Unknown'),
        })


class SearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        result = {
            'about_me': [],
            'about_prokope': [],
            'blog': [],
            'gallery': [],
        }

        if query:
            forbidden_patterns = re.compile(
                r'(DROP|SELECT|INSERT|DELETE|UPDATE|;|--)',
                re.IGNORECASE
            )
            if forbidden_patterns.search(query):
                return Response({
                    'error': 'Invalid search query. Please refine your input.',
                })

            about_me = Index.objects.filter(
                Q(about_me_title__icontains=query) |
                Q(about_me_description__icontains=query)
            )
            about_prokope = Index.objects.filter(
                Q(about_prokope_title__icontains=query) |
                Q(about_prokope_description__icontains=query)
            )

            tag_ids = TaggedItem.objects.filter(
                tag__name__icontains=query
            ).values_list('object_id', flat=True)

            blog = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(id__in=tag_ids)
            ).distinct()

            gallery = CountryAlbum.objects.filter(
                Q(country__name__icontains=query) |
                Q(title__icontains=query) |
                Q(city_galleries__city__name__icontains=query) |
                Q(city_galleries__photos__title__icontains=query) |
                Q(city_galleries__photos__caption__icontains=query)
            ).distinct()

            result = {
                'about_me': IndexSearchSerializer(about_me, many=True).data,
                'about_prokope': IndexSearchSerializer(about_prokope, many=True).data,
                'blog': BlogSearchSerializer(blog, many=True).data,
                'gallery': GallerySearchSerializer(gallery, many=True).data,
                'query': query,
            }

        return Response(result)
