# -*- coding: utf-8 -*-
# Django settings for ponyFiction project.
import os
from ponyFiction.apis.sphinxapi import SPH_MATCH_ALL, SPH_RANK_SPH04

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
DEBUG_TOOLBAR_CONFIG ={'INTERCEPT_REDIRECTS' : False}
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fanfics',                      # Or path to database file if using sqlite3.
        'USER': 'fanfics',                      # Not used with sqlite3.
        'PASSWORD': 'twilightsparkle',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False
MEDIA_ROOT = ''
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6^j694%m%^etq6@$_d&amp;1h$fv4z4-u!#@+*m233sc-39xdac3du'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)
ROOT_URLCONF = 'ponyFiction.urls'
ALLOWED_HOSTS = ['*']

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ponyFiction.wsgi.application'

import os.path
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'ponyFiction',
    'django.contrib.admin',
    'debug_toolbar',
    'registration',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
COMPRESS_HTML = True
SPHINX_CONFIG = {
    'server' : '/tmp/sphinx.socket',
    'retries_count' : 5,
    'retries_delay' : 1,
    'timeout' : 10,
    'match_mode' : SPH_MATCH_ALL,
    'rank_mode' : SPH_RANK_SPH04,
    'number' : 10,
    'max' : 1000,
    'cutoff' : 1000,
    'excerpts_opts' : {'chunk_separator' : '…', 'limit' : 2048, 'around' : 10, 'html_strip_mode' : 'strip'},
    'weights_stories' : {'title' : 100, 'summary' : 50, 'notes' : 25},
    'weights_chapters' : {'text' : 100, 'title' : 50, 'notes' : 25}
    }
COMMENTS_COUNT = {'page' : 50, 'main' : 5, 'stream' : 10, 'load': 50}
STORIES_COUNT = {'page' : 10, 'main' : 5, 'stream' : 10, 'load': 10}
CHAPTERS_COUNT = {'page' : 10, 'main' : 5, 'stream' : 10, 'load': 10}
COMMENTS_ORPHANS = 5
RSS = {'stories': 20, 'chapters': 20, 'comments': 100}
CUSTOM_USER_MODEL = 'ponyFiction.Author'
AUTHENTICATION_BACKENDS = ('ponyFiction.auth_backends.AuthorModelBackend',)
ACCOUNT_ACTIVATION_DAYS = 5
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@stories.everypony.ru'
RECAPTCHA_PUBLIC_KEY = '6LfbstoSAAAAAAcFIteoZTld24mt3s6_sODZnc8J'
RECAPTCHA_PRIVATE_KEY = '6LfbstoSAAAAAHHN9jYw9Lp9lsunQCILAyAYgoxz'
SANITIZER_ALLOWED_TAGS = [
    'b', 'i', 'strong', 'em', 's', 'u',
    'p', 'br', 'hr',
    'a',
    'ul', 'ol', 'li',
    'blockquote', 'sup', 'sub', 'pre', 'small', 'tt'
]

SANITIZER_ALLOWED_ATTRIBUTES = {
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'a': ['href', 'rel', 'title'],
}

SANITIZER_CHAPTER_ALLOWED_TAGS = [
    'b', 'i', 'strong', 'em', 's', 'u',
    'h3', 'h4', 'h5',
    'p', 'br', 'hr',
    'img', 'a',
    'ul', 'ol', 'li',
    'blockquote', 'sup', 'sub', 'pre', 'small', 'tt'
]

SANITIZER_CHAPTER_ALLOWED_ATTRIBUTES = {
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'a': ['href', 'rel', 'title'],
}

try:
    from local_settings import *
except ImportError:
    pass
