"""
Django settings for authors project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
from db_config import get_database_url
from corsheaders.defaults import default_headers
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7pgozr2jn7zs_o%i8id6=rddie!*0f0qy3$oy$(8231i^4*@u3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (Stylesheets, JS file, Images)
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'Token',
    'RedirectTo',
)

# Other places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'), )

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = [
    'ah-backend-stark-staging.herokuapp.com', 'ah-backend-stark.herokuapp.com',
    'localhost', '127.0.0.1'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'social_django',
    'authors.apps.authentication',
    'authors.apps.core',
    'authors.apps.profiles',
    'django_nose',
    'authors.apps.articles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'authors.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processor.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'authors.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {'default': dj_database_url.parse(get_database_url())}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation' +
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation' + '.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation' + '.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation' +
        '.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = ('0.0.0.0:4000', 'localhost:4000', 'localhost:3000',
                         'ah-frontend-stark.herokuapp.com')

# Tell Django about the custom `User` model we created. The string
# `authentication.User` tells Django we are referring to the `User` model in
# the `authentication` module. This module is registered above in a setting
# called `INSTALLED_APPS`.
AUTH_USER_MODEL = 'authentication.User'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'authors.apps.authentication.social_auth.views.create_social_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social_core.pipeline.disconnect.allowed_to_disconnect',
    'social_core.pipeline.disconnect.get_entries',
    'social_core.pipeline.disconnect.revoke_tokens',
    'social_core.pipeline.disconnect.disconnect',
)

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':
    'authors.apps.core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY':
    'error',
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('authors.apps.authentication.backends.JWTAuthentication', ),
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':
    10
}

if os.getenv('PRODUCTION', None):
    import django_heroku
    # Activate django-heroku
    django_heroku.settings(locals(), test_runner=False)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_SENDER')
EMAIL_HOST_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SOCIAL_AUTH_LOGIN_URL = '/api/social/login/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FACEBOOK_APP_ID')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email'}

SOCIAL_AUTH_TWITTER_KEY = os.getenv('TWITTER_APP_ID')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('TWITTER_SECRET')
SOCIAL_AUTH_TWITTER_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_TWITTER_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email'}
