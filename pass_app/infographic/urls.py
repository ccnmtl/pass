from .views import CreateInfographicItemView, UpdateInfographicItemView, \
    DeleteInfographicItemView, InfographicDetailView
from django.conf.urls import patterns

urlpatterns = patterns(
    'infographic.views',
    (r'^(?P<pk>\d+)/$', InfographicDetailView.as_view(), {},
     'infographic-detail'),
    (r'^(?P<pk>\d+)/add/item/$', CreateInfographicItemView.as_view(), {},
     'infographicitem-add'),
    (r'^edit/item/(?P<pk>[0-9]+)/$', UpdateInfographicItemView.as_view(), {},
     'infographicitem-update'),
    (r'^delete/item/(?P<pk>[0-9]+)/$', DeleteInfographicItemView.as_view(), {},
     'infographicitem-delete'),)
