"""
Django settings for gulflimo project.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-f7p4-35m)d9zdvtqj5d(sr_9l803_afa122a^6o#xai-!ue_4f')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED HOSTS - Trust Heroku domain and localhost
ALLOWED_HOSTS = [
    'gulflimo-f71ab9ca90c7.herokuapp.com',
    'localhost',
    '127.0.0.1',
    '.herokuapp.com',
]

# Application definition
INSTALLED_APPS = [
    'main_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Language middleware
]

ROOT_URLCONF = 'gulflimo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',  # Add CSRF context processor
                'main_app.context_processors.brand_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'gulflimo.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bahrain'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ar', 'العربية'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Simplified static file serving with whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication settings
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==================== CSRF & Security Settings ====================

# CSRF Trusted Origins - Allow Heroku domain
CSRF_TRUSTED_ORIGINS = [
    'https://gulflimo-f71ab9ca90c7.herokuapp.com',
    'https://*.herokuapp.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# CSRF Cookie Settings
CSRF_COOKIE_SECURE = True  # Only send cookie over HTTPS
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read (needed for AJAX)
CSRF_COOKIE_SAMESITE = 'Lax'  # Prevent cross-site cookie submission

# Session Cookie Settings
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Don't allow JS to read session
SESSION_COOKIE_SAMESITE = 'Lax'

# Security headers
SECURE_SSL_REDIRECT = not DEBUG  # Redirect HTTP to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Trust Heroku proxy
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# X-Frame-Options to prevent clickjacking
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'", 'https:'),
    'script-src': ("'self'", "'unsafe-inline'", 'https:'),
    'style-src': ("'self'", "'unsafe-inline'", 'https:'),
    'img-src': ("'self'", 'data:', 'https:'),
}
