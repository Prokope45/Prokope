"""Blog views.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView

from taggit.models import Tag
from git import Repo

from apps.blog.models import Post


# Blog Page
class TagMixin(object):
    """Mixin for taggit to be compatible with Prokope."""

    def get_context_data(self, **kwargs):
        """Get context data from taggit and adds the tags to the context."""
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tag'] = Tag.objects.all()
        return context


class TagIndexView(TagMixin, ListView):
    """Allows filtering by tags in the blog list."""
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Get all tags filtered by the tag slug."""
        return Post.objects.filter(tag__slug=self.kwargs.get('tag_slug'))


class PostList(TagMixin, ListView):
    """Blog post list."""

    model = Post
    template_name = 'post_list.html'
    # queryset = Post.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Allows for filtering/sorting by tags."""
        queryset = Post.objects.filter(status=1)

        sort_field = self.request.GET.get('sort', 'created_on')
        sort_order = self.request.GET.get('order', 'desc')

        # Handle sorting
        if sort_field in ['title', 'created_on', 'updated_on']:
            if sort_order == 'asc':
                queryset = queryset.order_by(sort_field)
            else:
                queryset = queryset.order_by(f'-{sort_field}')

        # Handle tag filtering
        tags = self.request.GET.getlist('tags')
        if tags:
            queryset = queryset.filter(tag__name__in=tags).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Get context data and add selected tags to the response."""
        context = super().get_context_data(**kwargs)
        # Add selected tags to the context for the template
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context


class PostDetail(DetailView):
    """Post detail view."""
    model = Post
    template_name = 'post_detail.html'


# GitHub-to-PythonAnywhere Update Webhook
@csrf_exempt
def update(request):
    """Update webook. Dead code."""
    if request.method == "POST":
        '''
        Pass the path of the directory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        '''
        repo = Repo("django-tech-blog")

        git = repo.git
        git.checkout('master')

        git.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse(
            "Couldn't update the code on PythonAnywhere",
        status=400)
