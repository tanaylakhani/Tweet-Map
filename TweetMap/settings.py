"""
Django settings for TweetMap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5e2pobd)$=qco1%xd3k7x6^+3p5s=-v_k)^$o05zmj)03rv)4b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'TweetMap.urls'
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'tweepy',
    'twitter_service',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'django.core.context_processors.media',
'django.core.context_processors.static',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
)
ROOT_URLCONF = 'TweetMap.urls'

WSGI_APPLICATION = 'TweetMap.wsgi.application'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
      os.path.join(os.path.dirname(__file__), 'templates/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tweetmap',
        'USER': 'root',
        'PASSWORD': 'tweetmap',
        'HOST': 'tweetmapdb.cisv9429qoli.us-east-1.rds.amazonaws.com',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_PATH, "dev")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.join(PROJECT_PATH, "TweetMap"), "static"),
)

try:
    from TweetMap.local_settings import *
except ImportError:
    try:
        from mod_python import apache
        apache.log_error( "local settings not available", apache.APLOG_NOTICE )
    except ImportError:
        import sys
        sys.stderr.write( "local settings not available\n" )
else:
    try:
        INSTALLED_APPS  += LOCAL_INSTALLED_APPS
    except NameError:
        pass

BROKER_URL = "sqs://%s:%s@" % (AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
CELERY_TIMEZONE = 'America/New_York'
CELERY_ACCEPT_CONTENT = ['pickle','json', 'msgpack', 'yaml']
from celery.schedules import crontab
from datetime import timedelta
