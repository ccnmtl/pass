# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

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


DEBUG = False
TEMPLATE_DEBUG = DEBUG
SENTRY_SITE = 'pass-staging'
STATSD_PREFIX = 'pass-staging'
STAGING_ENV = True

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

# AWS Settings for staging
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = "ccnmtl-pass-static-stage"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

# static data, e.g. css, js, etc.
STATIC_ROOT = "/tmp/pass/static"
STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
STATIC_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'

# uploaded images
MEDIA_URL = 'https://%s.s3.amazonaws.com/uploads/' % AWS_STORAGE_BUCKET_NAME

try:
    from local_settings import *
except ImportError:
    pass
