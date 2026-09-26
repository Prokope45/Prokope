from rest_framework import serializers
from taggit.models import Tag

from apps.blog.models import Contact, Post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'created_on',
            'updated_on', 'status', 'thumb', 'tag', 'content',
        ]

    def get_content(self, obj):
        return (obj.content or '')[:500]


class PostDetailSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
