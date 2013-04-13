from settings_shared import *

ADMINS = (
    ('CCNMTL-Kang', 'ccnmtl-sysadmin+staging@columbia.edu'),
)

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/pass/pass/pass_app/templates",
)

MEDIA_ROOT = '/usr/local/share/sandboxes/common/pass/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local_settings import *
except ImportError:
    pass
