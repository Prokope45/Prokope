from rest_framework import viewsets

from apps.index.api.serializers import IndexSerializer
from apps.index.models import Index


class IndexViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Index.objects.all().order_by('pk')
    serializer_class = IndexSerializer
    permission_classes = []
