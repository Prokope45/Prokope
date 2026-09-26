from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from taggit.models import Tag

from apps.blog.api.serializers import (
    ContactSerializer,
    PostDetailSerializer,
    PostListSerializer,
    TagSerializer,
)
from apps.blog.models import Contact, Post


class PostPagination(PageNumberPagination):
    """Match the Django template blog pagination of five posts per page."""

    page_size = 5


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status=1)
    lookup_field = 'slug'
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tag__name']
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_on', 'updated_on']
    ordering = ['-created_on']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(status=1)
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tag__name__in=tags).distinct()
        return queryset


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    pagination_class = None


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
