from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/match/match/templates",
)

MEDIA_ROOT = '/var/www/match/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/match/match/sitemedia'),	
)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local_settings import *
except ImportError:
    pass
