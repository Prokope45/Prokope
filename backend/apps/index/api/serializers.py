from rest_framework import serializers

from apps.index.models import Index


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'
