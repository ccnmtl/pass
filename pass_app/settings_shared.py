# Django settings for pass project.
import os.path
from ccnmtlsettings.shared import common

project = 'pass'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'pass_app.main',
    'pass_app.careerlocation',
    'pass_app.supportservices',
    'pass_app.specialneeds',
]

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'pass_app.main.views.context_processor'
)

ROOT_URLCONF = 'pass_app.urls'

INSTALLED_APPS += [  # noqa
    'django.contrib.humanize',
    'sorl.thumbnail',
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
    'pass_app.careerlocation',
    'pass_app.supportservices',
    'pass_app.infographic',
    'pass_app.specialneeds',
]

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = 'main.UserProfile'

PAGEBLOCKS = [
    'pageblocks.HTMLBlockWYSIWYG',
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
    'infographic.InfographicBlock',
    'specialneeds.SpecialNeedsCallBlock',
]

THUMBNAIL_SUBDIR = "thumbs"
