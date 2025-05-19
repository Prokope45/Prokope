from django.views.generic import ListView, DetailView

from gallery.models import PhotoGallery

# Gallery Page
class CountryGallery(ListView):
    model = PhotoGallery
    template_name = 'gallery.html'
    queryset = PhotoGallery.objects.all().order_by('country')
    context_object_name = 'gallery_info'


class CountryGalleryDetail(DetailView):
    model = PhotoGallery
    template_name = 'gallery_detail.html'
