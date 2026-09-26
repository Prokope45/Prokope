from rest_framework import serializers

from apps.blog.models import Post
from apps.gallery.models import CountryAlbum
from apps.index.models import Index


class IndexSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ['id', 'about_me_title', 'about_me_description', 'about_prokope_title', 'about_prokope_description']


class BlogSearchSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'tag']


class GallerySearchSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = CountryAlbum
        fields = ['id', 'title', 'slug', 'country']
