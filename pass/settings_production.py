from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/pass/pass/pass/templates",
)

MEDIA_ROOT = '/var/www/pass/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/pass/pass/sitemedia'),	
)

import logging
from sentry.client.handlers import SentryHandler
logger = logging.getLogger()
if SentryHandler not in map(lambda x: x.__class__, logger.handlers):
    logger.addHandler(SentryHandler())
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())

SENTRY_REMOTE_URL = 'http://sentry.ccnmtl.columbia.edu/sentry/store/'
# remember to set the SENTRY_KEY in a local_settings.py
# as documented in the wiki
SENTRY_SITE = 'pass'


DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local_settings import *
except ImportError:
    pass
