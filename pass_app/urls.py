from django.conf import settings
from django.conf.urls import include, patterns
from django.contrib import admin
from django.views.generic.base import TemplateView
from pass_app.api import UserResource
from pass_app.careerlocation.api import MapLayerResource, \
    ActorQuestionResource, ActorResource, ActorResponseResource, \
    CareerLocationStateResource, StrategyResource
from pass_app.supportservices.api import SupportServiceResource, \
    SupportServiceStateResource
from tastypie.api import Api
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(MapLayerResource())
v1_api.register(ActorQuestionResource())
v1_api.register(ActorResource())
v1_api.register(ActorResponseResource())
v1_api.register(CareerLocationStateResource())
v1_api.register(StrategyResource())
v1_api.register(SupportServiceResource())
v1_api.register(SupportServiceStateResource())

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))

logout_page = (r'^accounts/logout/$',
               'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
admin_logout_page = (r'^accounts/logout/$',
                     'django.contrib.auth.views.logout',
                     {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$',
                   'djangowind.views.logout',
                   {'next_page': redirect_after_logout})
    admin_logout_page = (r'^admin/logout/$',
                         'djangowind.views.logout',
                         {'next_page': redirect_after_logout})


urlpatterns = patterns(
    '',
    logout_page,
    admin_logout_page,
    auth_urls,
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

    (r'^admin/', include(admin.site.urls)),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^_infographic/', include('pass_app.infographic.urls')),
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
    (r'^module-four/(?P<path>.*)$', 'pass_app.main.views.module_four'),
    (r'^module-five/(?P<path>.*)$', 'pass_app.main.views.module_five'),

    (r'^api/', include(v1_api.urls))
)
