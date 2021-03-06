import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/pass/pass/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/pass/pass/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pass_app.settings_production'

import django.core.handlers.wsgi
import django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()
