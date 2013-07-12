# flake8: noqa
from pass_app.settings import *

TEMPLATE_DIRS = (
    "/var/www/pass/pass/pass_app/templates",
)

MEDIA_ROOT = '/var/www/pass/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/pass/pass/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pass',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/pass/pass/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEV_ENV = True

STATSD_PREFIX = 'pass-dev'
SENTRY_SITE = 'pass-dev'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    import logging
    from sentry.client.handlers import SentryHandler
    logger = logging.getLogger()
    if SentryHandler not in map(lambda x: x.__class__, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
