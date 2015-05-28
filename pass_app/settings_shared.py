# Django settings for pass project.
import os.path
import sys


DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']

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

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['pass_app.main',
                'pass_app.careerlocation',
                'pass_app.supportservices']

DEFAULT_FROM_EMAIL = 'pass@pass.ccnmtl.columbia.edu'
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/pass/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'djangowind.context.context_processor',
    'django.core.context_processors.static',
    'stagingcontext.staging_processor',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'pass_app.urls'

TEMPLATE_DIRS = (
    "/var/www/pass/pass_app/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'django.contrib.admin',
    'tagging',
    'smartif',
    'template_utils',
    'typogrify',
    'bootstrapform',
    'pagetree',
    'pageblocks',
    'pass_app.main',
    'quizblock',
    'careermapblock',
    'registration',
    'responseblock',
    'proxyblock',
    'django_statsd',
    'pass_app.careerlocation',
    'django_jenkins',
    'smoketest',
    'waffle',
    'compressor',
    'django_markwhat',
    'pass_app.supportservices',
    'pass_app.infographic',
]

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'pass'
STATSD_HOST = 'localhost'
STATSD_PORT = 8125

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = 'main.UserProfile'

PAGEBLOCKS = ['pageblocks.HTMLBlockWYSIWYG',
              'pageblocks.TextBlock',
              'pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'pageblocks.ImageBlock',
              'pageblocks.ImagePullQuoteBlock',
              'quizblock.Quiz',
              'careermapblock.CareerMap',
              'responseblock.Response',
              'proxyblock.ProxyBlock',
              'careerlocation.CareerLocationBlock',
              'careerlocation.CareerLocationSummaryBlock',
              'careerlocation.CareerLocationStrategyBlock',
              'supportservices.SupportServiceBlock',
              'infographic.InfographicBlock']


THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[pass] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "pass@ccnmtl.columbia.edu"

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

# WIND settings
AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend', )
CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', 'jb2410', 'zm4', 'sbd12',
                                'egr2107', 'kmh2124', 'sld2131',
                                'amm8', 'mar227', 'ed2198', 'cks2120']
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
