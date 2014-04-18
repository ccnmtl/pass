# flake8: noqa
from pass_app.settings import *

TEMPLATE_DIRS = (
    "/var/www/pass/pass/pass_app/templates",
)

COMPRESS_ROOT = "/var/www/pass/pass/media/"

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

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEV_ENV = True

try:
    from local_settings import *
except ImportError:
    pass
