from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db.models import Q

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView

from taggit.models import Tag, TaggedItem
from git import Repo

from .forms import ContactForm
from .models import Index, Post, PhotoGallery

from photologue.models import Gallery, Photo

import re
import random

# Custom Error Pages
def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})


# Index/Home Page
def index_view(request):
    context = {
        'index_data': Index.objects.first(),
        'posts': Post.objects.filter(status=1).order_by('-updated_on')[:2],
    }
    # if (len(PhotoGallery.objects.all()) > 0):
    random_gallery = random.choice(PhotoGallery.objects.all())
    context['carousel_gallery_name'] =  random_gallery
    context['carousel_photos'] = random.choice(random_gallery.galleries.all())
    return render(request, 'index.html', context)


# Blog Page
class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tag'] = Tag.objects.all()
        return context


class TagIndexView(TagMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tag__slug=self.kwargs.get('tag_slug'))


class PostList(TagMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    # queryset = Post.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        # Add selected tags to the context for the template
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'


# Gallery Page
class CountryGallery(ListView):
    model = PhotoGallery
    template_name = 'gallery.html'
    queryset = PhotoGallery.objects.all().order_by('country')
    context_object_name = 'gallery_info'


class CountryGalleryDetail(DetailView):
    model = PhotoGallery
    template_name = 'gallery_detail.html'

def search(request):
    query = request.GET.get('q', '').strip()

    about_me_results = []
    plans_results = []
    blog_results = []
    gallery_results = []
    error_message = None

    if query:
        forbidden_patterns = re.compile(r'(DROP|SELECT|INSERT|DELETE|UPDATE|;|--)', re.IGNORECASE)

        if forbidden_patterns.search(query):
            error_message = "Invalid search query. Please refine your input."
            query = ''  # Clear the query to prevent further processing
        else:
            about_me_results = Index.objects.filter(
                Q(about_me_title__icontains=query) |
                Q(about_me_description__icontains=query)
            )
            about_prokope_results = Index.objects.filter(
                Q(about_prokope_title__icontains=query) |
                Q(about_prokope_description__icontains=query)
            )

            tag_ids = TaggedItem.objects.filter(tag__name__icontains=query).values_list('object_id', flat=True)

            blog_results = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(id__in=tag_ids)  # Search in tags
            ).distinct()

            gallery_results = PhotoGallery.objects.filter(
                Q(country__icontains=query) |
                Q(content__icontains=query) |
                Q(galleries__title__icontains=query) |
                Q(galleries__description__icontains=query)
            ).distinct()

    context = {
        'index_results': {
            'about_me': about_me_results,
            'about_prokope': about_prokope_results,
        },
        'blog_results': blog_results,
        'gallery_results': gallery_results,
        'query': query,
        'error_message': error_message,
    }

    return render(request, 'search_results.html', context)

# GitHub-to-PythonAnywhere Update Webhook
@csrf_exempt
def update(request):
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
        return HttpResponse("Couldn't update the code on PythonAnywhere", status=400)
