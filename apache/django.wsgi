import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/match/match/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/match/')
sys.path.append('/var/www/match/match/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'match.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
