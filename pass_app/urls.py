import django.contrib.auth.views
import django.views.static
import djangowind.views

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from tastypie.api import Api

from pass_app.api import UserResource
from pass_app.careerlocation.api import MapLayerResource, \
    ActorQuestionResource, ActorResource, ActorResponseResource, \
    CareerLocationStateResource, StrategyResource
from pass_app.main.views import (
    PassDetailedResults, intro, exporter, importer, clear_state,
    all_results_key, reports, edit_page, instructor_page, demographic,
    module_one, module_two, module_three, module_four, module_five,
)
from pass_app.supportservices.api import SupportServiceResource, \
    SupportServiceStateResource


admin.autodiscover()

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

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))

logout_page = url(r'^accounts/logout/$',
                  django.contrib.auth.views.logout,
                  {'next_page': redirect_after_logout})
admin_logout_page = url(r'^accounts/logout/$',
                        django.contrib.auth.views.logout,
                        {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))
    logout_page = url(r'^accounts/logout/$',
                      djangowind.views.logout,
                      {'next_page': redirect_after_logout})
    admin_logout_page = url(r'^admin/logout/$',
                            djangowind.views.logout,
                            {'next_page': redirect_after_logout})


urlpatterns = [
    logout_page,
    admin_logout_page,
    auth_urls,
    url(r'^$', intro),

    url(r'^about/', TemplateView.as_view(template_name='main/about.html')),
    url(r'^help/', TemplateView.as_view(template_name='main/help.html')),

    url(r'^export/$', exporter),
    url(r'^import/$', importer),
    url(r'^admin/_clear_state/$', clear_state),
    url('^admin/allresults/$', PassDetailedResults.as_view()),
    url('^admin/allresultskey/$', all_results_key),
    url(r'^admin/reports/(?P<path>.*)$', reports),
    url(r'^registration/', include('registration.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^_quiz/', include('quizblock.urls')),
    url(r'^quizblock/', include('quizblock.urls')),
    url(r'^_infographic/', include('pass_app.infographic.urls')),
    url(r'^_specialneeds/', include('pass_app.specialneeds.urls')),
    url(r'^_careermap/', include('careermapblock.urls')),
    url(r'^_careerlocation/', include('pass_app.careerlocation.urls')),
    url(r'^_stats/$', TemplateView.as_view(template_name="main/stats.html")),

    url(r'^(?P<hierarchy>[\w\-]+)/edit/(?P<path>.*)$', edit_page),

    url(r'^instructor/(?P<path>.*)$', instructor_page),
    url(r'^demographic/(?P<path>.*)$', demographic),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^module-one/(?P<path>.*)$', module_one),
    url(r'^module-two/(?P<path>.*)$', module_two),
    url(r'^module-three/(?P<path>.*)$', module_three),
    url(r'^module-four/(?P<path>.*)$', module_four),
    url(r'^module-five/(?P<path>.*)$', module_five),

    url(r'^api/', include(v1_api.urls)),
]
