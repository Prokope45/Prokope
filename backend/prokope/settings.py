"""
Developer: Jared Paubel
"""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
TEMPLATES_DIRS = os.path.join(BACKEND_DIR, 'templates')

dotenv_file = os.path.join(BACKEND_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file, override=True)

SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT in ['QA', 'development']
CONNECTED_TO_PRODUCTION_DB = ENVIRONMENT == "production"

# The `DYNO` env var is set on Heroku CI, but it's not a real Heroku app, so we have to
# also explicitly exclude CI:
# https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables
IS_HEROKU_APP = "DYNO" in os.environ and "CI" not in os.environ

if IS_HEROKU_APP:
    # On Heroku, it's safe to use a wildcard for `ALLOWED_HOSTS`, since the Heroku router performs
    # validation of the Host header in the incoming HTTP request. On other platforms you may need to
    # list the expected hostnames explicitly in production to prevent HTTP Host header attacks. See:
    # https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-ALLOWED_HOSTS
    ALLOWED_HOSTS = ["*"]

    # Redirect all non-HTTPS requests to HTTPS. This requires that:
    # 1. Your app has a TLS/SSL certificate, which all `*.herokuapp.com` domains do by default.
    #    When using a custom domain, you must configure one. See:
    #    https://devcenter.heroku.com/articles/automated-certificate-management
    # 2. Your app's WSGI web server is configured to use the `X-Forwarded-Proto` headers set by
    #    the Heroku Router (otherwise you may encounter infinite HTTP 301 redirects). See this
    #    app's `gunicorn.conf.py` for how this is done when using gunicorn.
    #
    # For maximum security, consider enabling HTTP Strict Transport Security (HSTS) headers too:
    # https://docs.djangoproject.com/en/5.2/ref/middleware/#http-strict-transport-security
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = [
        'www.prokope.io',
        'localhost',
        '127.0.0.1'
    ]

# Controls whether forward slash should be appended to endpoints
# Since the OIDC IdP looks for webfinger, it strictly requires that 
# no slash is appended to the endpoint.
APPEND_SLASH = True

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'hcaptcha',
    'crispy_forms',
    'django_summernote',
    'apps.common',
    'apps.index',
    'apps.blog',
    'apps.gallery',
    'apps.oidc.apps.AppConfig',
    'photologue',
    'sortedm2m',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'taggit',
    'storages',
    "mozilla_django_oidc",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.oidc.backends.PocketIDBackend"
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Prokope API",
    "DESCRIPTION": "REST API for Prokope personal portfolio and travel blog",
    "VERSION": "1.0.0",
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/"

ADMIN_OIDC_CLIENT_ENABLED = os.environ.get('ADMIN_OIDC_CLIENT_ENABLED', "")

OIDC_USE_PKCE = os.environ.get('OIDC_USE_PKCE', "")
OIDC_PKCE_CODE_VERIFIER_SIZE = int(os.environ.get('OIDC_PKCE_CODE_VERIFIER_SIZE', "0"))

OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ.get('OIDC_OP_AUTHORIZATION_ENDPOINT', "")
OIDC_OP_TOKEN_ENDPOINT = os.environ.get('OIDC_OP_TOKEN_ENDPOINT', "")
OIDC_OP_USER_ENDPOINT = os.environ.get('OIDC_OP_USER_ENDPOINT', "")
OIDC_OP_JWKS_ENDPOINT = os.environ.get('OIDC_OP_JWKS_ENDPOINT', "")

# Client credentials
OIDC_RP_CLIENT_ID = os.environ.get('OIDC_RP_CLIENT_ID', "")
OIDC_RP_CLIENT_SECRET = os.environ.get('OIDC_RP_CLIENT_SECRET', "")
OIDC_RP_SIGN_ALGO = os.environ.get('OIDC_RP_SIGN_ALGO', "")
OIDC_RP_SCOPES = os.environ.get('OIDC_RP_SCOPES', "")

# Taggit set case as insensitive
TAGGIT_CASE_INSENSITIVE = True

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'apps.common.middleware.SPAMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
]

ROOT_URLCONF = 'prokope.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIRS],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

WSGI_APPLICATION = 'prokope.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


def test_database_config() -> dict[str, str]:
    print("NOTE: Using 'test_db' database for testing and development.")
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'user',
            'PASSWORD': 'password',
            'HOST': 'db',
            'PORT': '5432',
        }
    }


def qa_database_config() -> dict[str, str]:
    print("NOTE: Using 'dev_db' database for QA testing.\n This is a copy of the production database.")
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'dev_db',
            'USER': 'user',
            'PASSWORD': 'password',
            'HOST': 'dev_db',
            'PORT': '5432',
        }
    }


def prod_database_config():
    if url := os.environ.get('DATABASE_URL', ""):
        print("Using database URI...")
        parsed = urlparse(url)
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': parsed.path[1:],
                'USER': parsed.username,
                'PASSWORD': parsed.password,
                'HOST': parsed.hostname,
                'PORT': parsed.port,
            }
        }
    else:
        print("Using specified variables...")
        # Try the specified variables
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DATABASE_NAME', ""),
                'USER': os.environ.get('DATABASE_USER', ""),
                'PASSWORD': os.environ.get('DATABASE_PASSWORD', ""),
                'HOST': os.environ.get('DATABASE_HOST', ""),
                'PORT': '5432',
            }
        }


if IS_HEROKU_APP:
    # Note: this is the only branch that derives ENGINE from the DATABASE_URL
    # scheme, so it is the only one that would need a non-postgres driver
    # (e.g. MySQLdb) installed. We ship postgres only -- keep DATABASE_URL
    # postgres:// or this will fail at connect time.
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
elif ENVIRONMENT == 'development' or ('test' in sys.argv or 'test_coverage' in sys.argv):
    DATABASES = test_database_config()
elif ENVIRONMENT == 'QA':
    DATABASES = qa_database_config()
elif ENVIRONMENT == 'production':
    print("NOTE: Connected to PRODUCTION database.")
    DATABASES = prod_database_config()

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'dist'),
    os.path.join(BACKEND_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BACKEND_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Base url to serve media files
if IS_HEROKU_APP or ENVIRONMENT == "QA":
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_VERIFY = True
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', "")
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', "")
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', "")
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/'
    # DEFAULT_FILE_STORAGE = 'prokope.storage_backends.MediaStorage'
    STORAGES = {
        "default": {
            "BACKEND": 'prokope.storage_backends.MediaStorage',
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BACKEND_DIR, 'media/')


# For Summernote WYSIWYG
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Contact Form Email Settings
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', "")
# Temp: used for local testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', "")
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', "")
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', "")
EMAIL_PORT = os.environ.get('EMAIL_PORT', "")
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', "")
DEFAULT_FROM_EMAIL= os.environ.get('DEFAULT_FROM_EMAIL', "")

# Bootstrap Messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Hcaptcha Verification
HCAPTCHA_SITEKEY = os.environ.get('HCAPTCHA_SITEKEY', "")
HCAPTCHA_SECRET = os.environ.get('HCAPTCHA_SECRET', "")
VERIFY_URL = os.environ.get('VERIFY_URL', "")
