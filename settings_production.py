from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/pass/pass/templates",
)

MEDIA_ROOT = '/var/www/pass/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/pass/pass/sitemedia'),	
)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local_settings import *
except ImportError:
    pass
