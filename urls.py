from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       (r'^$','main.views.intro'),

                       (r'^export/$','main.views.exporter'),
                       (r'^import/$','main.views.importer'),
                       (r'^registration/', include('registration.urls')),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^munin/',include('munin.urls')),
                       (r'^pagetree/',include('pagetree.urls')),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
                       (r'^_quiz/',include('quizblock.urls')),
                       (r'^_careermap/',include('careermapblock.urls')),
                       (r'^edit/(?P<path>.*)$','pass.main.views.edit_page',{},'edit-page'),
                       (r'^instructor/(?P<path>.*)$','pass.main.views.instructor_page'),
                       (r'^(?P<path>.*)$','pass.main.views.page'),
                       
) 

