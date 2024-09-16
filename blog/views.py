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
from .models import IndexDescription, Post, PhotoGallery

from photologue.models import Gallery, Photo

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
        'index_data': IndexDescription.objects.all(),
        'posts': Post.objects.filter(status=1).order_by('-updated_on')[:2]
    }
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
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'


# Gallery Page
class Gallery(ListView):
    model = PhotoGallery
    template_name = 'gallery.html'
    queryset = PhotoGallery.objects.all().order_by('country')
    context_object_name = 'gallery_info'


class GalleryDetail(DetailView):
    model = PhotoGallery
    template_name = 'gallery_detail.html'

def search(request):
    # TODO: Implement search in gallery and index pages.
    query = request.GET.get('q')
    results = []

    if query:
        tag_ids = TaggedItem.objects.filter(tag__name__icontains=query).values_list('object_id', flat=True)

        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(id__in=tag_ids)  # Search in tags
        ).distinct()

    context = {
        'results': results,
        'query': query,
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
