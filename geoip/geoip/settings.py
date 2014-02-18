"""
Django settings for geoip project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

LOCAL = os.environ.get("LOCAL")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

try:
    execfile(SITE_ROOT + '/../config.py')
except IOError as e:
    execfile(SITE_ROOT + '/config.py')
    print "Unable to open configuration file!", e

if LOCAL:  # export LOCAL=1
    DEBUG = True
    POSTGRES = POSTGRES_LOCAL


DEBUG_TOOLBAR_PATCH_SETTINGS = False
SOUTH_TESTS_MIGRATE = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

ADMINS = (
    ('jblum', 'jblum@cbitlabs.com'),
)

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES["NAME"],  # Or path to database file if using sqlite3.
        'USER': POSTGRES["USER"],  # Not used with sqlite3.
        'PASSWORD': POSTGRES["PASSWORD"],  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': POSTGRES["HOST"],
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',

    # third party
    'gunicorn',
    'south',
    'kronos',

    # geoip
    'api',
    'ratings',
    'common'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "templates"),
)

ROOT_URLCONF = 'geoip.urls'

WSGI_APPLICATION = 'geoip.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version':
    1,
    'disable_existing_loggers':
    False,
    'filters':
    {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers':
    {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers':
    {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
