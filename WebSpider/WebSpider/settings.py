"""
Django settings for WebSpider project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from __future__ import absolute_import
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#import djcelery
#djcelery.setup_loader()


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CELERY_TASK_SERIALIZER = "json"
CELERYD_MAX_TASKS_PER_CHILD = 1
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nxw)+fd#=c9t%tsy@4rmpne)f(x+q#)$gyk)!@xb8#2-0h3^0%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
# Application definition

BROKER_URL = 'django://' 

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crawler',
    'kombu.transport.django',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'WebSpider.urls'

WSGI_APPLICATION = 'WebSpider.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login/'


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "templates"),
)

if DEBUG:
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static-only")
    MEDIA_ROOT =  os.path.join(os.path.dirname(BASE_DIR), "static", "media") 
    STATICFILES_DIRS = (
                    os.path.join(os.path.dirname(BASE_DIR), "static", "static"),
                    )

