from django.contrib.admin.apps import AdminConfig


class AppConfig(AdminConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.oidc'

    def ready(self):
        self.module.default_app_config = __name__
        from django.contrib import admin
        from .admin import HybridAdminSite
        admin.site.__class__ = HybridAdminSite
