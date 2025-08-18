"""
Fly.io optimized Django settings for whsxc project.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)  # Temporarily enabled for debugging

# Fly.io specific host configuration
FLY_APP_NAME = config('FLY_APP_NAME', default='whsxc')
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'whsxc.com',
    'dev.whsxc.com',
    'www.whsxc.com',
    'whsxc.fly.dev',  # Fly.io domain
    f'{FLY_APP_NAME}.fly.dev',  # Default Fly.io domain
]

# Add any additional hosts from environment
ADDITIONAL_HOSTS = config('ADDITIONAL_HOSTS', default='')
if ADDITIONAL_HOSTS:
    ALLOWED_HOSTS.extend([host.strip() for host in ADDITIONAL_HOSTS.split(',') if host.strip()])

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "blog",
    "runners",
    "meets",
    "history",
    "schedule",
    "homemeet",
    "runninglinks",
    "summerrunning",
    "simplemenu",
    "crosscountry",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For serving static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]

ROOT_URLCONF = "whsxc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "whsxc.wsgi.application"

# Database configuration for Fly.io
# Use persistent volume if available, otherwise ephemeral storage
DATABASE_PATH = config('DATABASE_PATH', default='/app/data/running.db')
if not os.path.exists(os.path.dirname(DATABASE_PATH)):
    # Fallback to app directory if persistent volume not available
    DATABASE_PATH = BASE_DIR / "running.db"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_PATH,
        "OPTIONS": {
            'timeout': 20,  # Prevent database locks
        }
    }
}

# Optional PostgreSQL configuration (uncomment and set env vars to use)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DATABASE_URL').split('/')[-1],
#         'USER': config('DATABASE_URL').split('://')[1].split(':')[0],
#         'PASSWORD': config('DATABASE_URL').split('://')[1].split(':')[1].split('@')[0],
#         'HOST': config('DATABASE_URL').split('@')[1].split(':')[0],
#         'PORT': config('DATABASE_URL').split(':')[-1].split('/')[0],
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files configuration for Fly.io
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# WhiteNoise configuration for static file serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CSRF settings for Fly.io
CSRF_TRUSTED_ORIGINS = [
    'https://whsxc.com',
    'https://dev.whsxc.com',
    'https://www.whsxc.com',
    f'https://{FLY_APP_NAME}.fly.dev',
]

# Add localhost for local testing
if DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        'https://localhost',
        'http://localhost',
    ])

# HTTPS settings for production
if not DEBUG:
    # SECURE_SSL_REDIRECT = True  # Disabled - Fly.io handles HTTPS redirect
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Site ID for django.contrib.sites (required for flatpages)
SITE_ID = 1

# Logging configuration for Fly.io
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'whsxc': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Fly.io specific settings
if config('FLY_APP_NAME', default=None):
    # Running on Fly.io

    # Use Fly.io's internal networking
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]

    # Email configuration (if needed)
    EMAIL_BACKEND = config(
        'EMAIL_BACKEND',
        default='django.core.mail.backends.console.EmailBackend'
    )

    # Session configuration
    SESSION_COOKIE_AGE = 86400  # 1 day
    SESSION_SAVE_EVERY_REQUEST = True

    # Cache configuration (optional - can use Redis if needed)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Performance settings (disabled for debugging)
# if not DEBUG:
#     # Enable template caching in production
#     TEMPLATES[0]['APP_DIRS'] = False  # Must be False when loaders are defined
#     TEMPLATES[0]['OPTIONS']['loaders'] = [
#         ('django.template.loaders.cached.Loader', [
#             'django.template.loaders.filesystem.Loader',
#             'django.template.loaders.app_directories.Loader',
#         ]),
#     ]
