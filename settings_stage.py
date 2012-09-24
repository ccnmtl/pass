from settings_shared import *

ADMINS = (
    ('CCNMTL-Kang', 'ccnmtl-sysadmin+staging@columbia.edu'),
    )

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/pass/pass/templates",
    )

MEDIA_ROOT = '/usr/local/share/sandboxes/common/pass/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG
