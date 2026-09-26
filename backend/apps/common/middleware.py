import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse


class SPAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        skip_prefixes = (
            '/admin',
            '/api',
            '/oidc',
            '/summernote',
            '/photologue',
            '/media',
            '/static',
            '/.well-known',
            '/blog/update_server',
        )
        if request.path.startswith(skip_prefixes):
            return self.get_response(request)

        dist_path = Path(settings.BASE_DIR) / 'frontend' / 'dist'

        # Serve actual files (CSS, JS, images, etc.) from the dist directory
        relative_path = request.path.lstrip('/')
        asset_path = dist_path / relative_path
        if asset_path.exists() and asset_path.is_file():
            content_type, _ = mimetypes.guess_type(str(asset_path))
            return FileResponse(
                open(asset_path, 'rb'),
                content_type=content_type or 'application/octet-stream'
            )

        # Serve index.html for SPA client-side routing
        index_path = dist_path / 'index.html'
        if index_path.exists():
            with open(index_path) as f:
                return HttpResponse(f.read(), content_type='text/html; charset=utf-8')

        return self.get_response(request)
