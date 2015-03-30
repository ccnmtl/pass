import os, sys, site

site.addsitedir('/var/www/pass/pass/ve/lib/python2.7/site-packages')
sys.path.append('/var/www/pass/pass/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pass_app.settings_staging'

import django.core.handlers.wsgi
import django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()
