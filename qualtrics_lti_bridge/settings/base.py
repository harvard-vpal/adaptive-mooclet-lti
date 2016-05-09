"""
Django settings for qualtrics_lti_bridge project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import abspath, basename, dirname, join, normpath
from django.core.urlresolvers import reverse_lazy
from sys import path
from .secure import SECURE_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute filesystem path to the Django project config directory:
# (this is the parent of the directory where this file resides,
# since this file is now inside a 'settings' pacakge directory)
DJANGO_PROJECT_CONFIG = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
# (this is one directory up from the project config directory)
SITE_ROOT = dirname(DJANGO_PROJECT_CONFIG)

# Site name:
SITE_NAME = basename(SITE_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(SITE_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

## moved to TEMPLATE dict
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qlb',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'cached_auth.Middleware',
    'django_auth_lti.middleware.LTIAuthMiddleware',
    ## from new version of icommons django-auth-lti
    # 'django_auth_lti.middleware_patched.MultiLTILaunchAuthMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
AUTHENTICATION_BACKENDS = (
    'django_auth_lti.backends.LTIAuthBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = reverse_lazy('lti_auth_error')

ROOT_URLCONF = 'qualtrics_lti_bridge.urls'

WSGI_APPLICATION = 'qualtrics_lti_bridge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Note - if you configure a database, you can store the database
# access credentials in the secure.py file. Just make sure that
# you do not remove secure.py from the .gitignore file. secure.py
# should never be uploaded to git. Secure.py.example is there to
# show you what secure.py should look like.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/lti_tools/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(SITE_ROOT, 'static')),
)
STATIC_ROOT = normpath(join(SITE_ROOT, 'http_static'))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', None)

## for dce version of django-auth-lti
from oauthlib.oauth1 import RequestValidator
LTI_REQUEST_VALIDATOR = 'qlb.validator.LTIRequestValidator'

# TEMPLATES = [{
#     'DEBUG': True,
#     'OPTIONS':{
#         # 'context_processors': [
#         #     # access the request inside django template
#         #     # 'django.core.context_processors.request'
#         # ],
#     },
#     'DIRS':[
#         normpath(join(SITE_ROOT, 'static')),
#     ],
#     # List of callables that know how to import templates from various sources.
#     'TEMPLATE_LOADERS':[
#         'django.template.loaders.filesystem.Loader',
#         'django.template.loaders.app_directories.Loader',
#     ],
# },]

