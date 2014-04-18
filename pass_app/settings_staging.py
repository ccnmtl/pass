# flake8: noqa
from settings_shared import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pass',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/pass/pass/media/"

TEMPLATE_DIRS = (
    "/var/www/pass/pass/pass_app/templates",
)

MEDIA_ROOT = '/var/www/pass/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/pass/pass/sitemedia'),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SENTRY_SITE = 'pass-staging'
STATSD_PREFIX = 'pass-staging'
STAGING_ENV = True

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
