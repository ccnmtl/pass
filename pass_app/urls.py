from django.conf.urls.defaults import include, patterns
from django.contrib import admin
from django.conf import settings
import os.path
from django.views.generic import TemplateView
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'^$', 'pass_app.main.views.intro'),

    (r'^about/', TemplateView.as_view(template_name='main/about.html')),
    (r'^help/', TemplateView.as_view(template_name='main/help.html')),

    (r'^export/$', 'pass_app.main.views.exporter'),
    (r'^import/$', 'pass_app.main.views.importer'),
    (r'^download/(?P<filename>\w[^/]*)/$', 'pass_app.main.views.download'),
    (r'^admin/_clear_state/$', 'pass_app.main.views.clear_state'),
    ('^admin/allresults/$', 'pass_app.main.views.all_results'),
    ('^admin/allresultskey/$', 'pass_app.main.views.all_results_key'),
    (r'^admin/reports/(?P<path>.*)$', 'pass_app.main.views.reports'),
    (r'^registration/', include('registration.urls')),
    ('^accounts/', include('djangowind.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^munin/', include('munin.urls')),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^logout/$',
     'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^_careermap/', include('careermapblock.urls')),
    (r'^_careerlocation/', include('pass_app.careerlocation.urls')),
    (r'^_stats/$', TemplateView.as_view(template_name="main/stats.html")),

    (r'^(?P<hierarchy>[\w\-]+)/edit/(?P<path>.*)$',
     'pass_app.main.views.edit_page'),

    (r'^instructor/(?P<path>.*)$',
     'pass_app.main.views.instructor_page'),
    (r'^demographic/(?P<path>.*)$',
     'pass_app.main.views.demographic'),
    (r'smoketest/', include('smoketest.urls')),
    (r'^module-one/(?P<path>.*)$', 'pass_app.main.views.module_one'),
    (r'^module-two/(?P<path>.*)$', 'pass_app.main.views.module_two'),
    (r'^module-three/(?P<path>.*)$', 'pass_app.main.views.module_three'),
    (r'^module-four/(?P<path>.*)$', 'pass_app.main.views.module_four')
)
