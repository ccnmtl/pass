import os, sys, site

# enable the virtualenv
site.addsitedir('/usr/local/share/sandboxes/common/pass/pass/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/usr/local/share/sandboxes/common/pass/pass/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pass.settings_stage'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
