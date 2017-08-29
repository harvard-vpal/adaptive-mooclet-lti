"""
Django settings for adaptive_mooclet_lti project.

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
SECRET_KEY = SECURE_SETTINGS.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ## external apps
    'storages',
    'rest_framework',
    'ordered_model',
    'bootstrap3',
    'django_bootstrap_breadcrumbs',
    # 'crispy_forms',

    ## core functions
    'lti',
    'engine',
    'quiz',
    'qualtrics',
    'api',

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
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'adaptive_mooclet_lti.middleware.XFrameOptionsMiddleware',
    #'adaptive_mooclet_lti.middleware.CookielessSessionMiddleware',
)
AUTHENTICATION_BACKENDS = (
    'django_auth_lti.backends.LTIAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS':[
        normpath(join(SITE_ROOT, 'templates')),
    ],
    'OPTIONS':{
        'context_processors': [
            # django auth
            'django.contrib.auth.context_processors.auth',

            # access the request inside django template
            'django.template.context_processors.request',
            # 'django.template.context_processors.debug',

            # enable django messages
            'django.contrib.messages.context_processors.messages',
        ],
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'debug':True,
    },
},]

LOGIN_URL = reverse_lazy('lti_auth_error')

ROOT_URLCONF = 'adaptive_mooclet_lti.urls'

WSGI_APPLICATION = 'adaptive_mooclet_lti.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Note - if you configure a database, you can store the database
# access credentials in the secure.py file. Just make sure that
# you do not remove secure.py from the .gitignore file. secure.py
# should never be uploaded to git. Secure.py.example is there to
# show you what secure.py should look like.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SECURE_SETTINGS.get('db_name'),
        'USER': SECURE_SETTINGS.get('db_user'),
        'PASSWORD': SECURE_SETTINGS.get('db_pass'),
        'HOST': SECURE_SETTINGS.get('db_host'),
        'PORT': SECURE_SETTINGS.get('db_port'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True

SESSION_SAVE_EVERY_REQUEST = True

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(SITE_ROOT, 'static')),
)



#### AMAZON S3 STATICFILES STORAGE ####
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = SECURE_SETTINGS.get('AWS_STORAGE_BUCKET_NAME', None)
AWS_S3_ACCESS_KEY_ID = SECURE_SETTINGS.get('AWS_S3_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = SECURE_SETTINGS.get('AWS_SECRET_ACCESS_KEY', None)

#### crispy-forms ####
# CRISPY_TEMPLATE_PACK = 'bootstrap3'

#### django-bootstrap ####
BOOTSTRAP3 = {
    'include_jquery':True,
}

#####################
#### LTI-related ####
#####################

LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('LTI_OAUTH_CREDENTIALS', None)

## for dce version of django-auth-lti
from oauthlib.oauth1 import RequestValidator
LTI_REQUEST_VALIDATOR = 'lti.validator.LTIRequestValidator'


###############################################
#### APP SETTINGS FOR ADAPTIVE-MOOCLET-LTI ####
###############################################

# Qualtrics API token
QUALTRICS_API_TOKEN = SECURE_SETTINGS.get('qualtrics_api_token')
QUALTRICS_USER = SECURE_SETTINGS.get('qualtrics_user')
# Qualtrics base url for making API (v3) calls
QUALTRICS_BASE_URL = SECURE_SETTINGS.get('qualtrics_base_url','https://yourdatacenterid.qualtrics.com')

# Qualtrics base url for making API (v2) calls
QUALTRICS_API_URL = 'https://survey.qualtrics.com/WRAPI/ControlPanel/api.php'

# QSF template name, assumes it is in static/qualtrics
QUALTRICS_TEMPLATE_NAME = 'MOOClet_template.qsf'
QSF_ROOT = normpath(join(SITE_ROOT, 'static/qsf'))


#### DJANGO REST FRAMEWORK SETTINGS ####

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


