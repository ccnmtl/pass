from django.conf.urls import patterns, url
from .views import (EditInfographicView, CreateInfographicItemView,
                    UpdateInfographicItemView, DeleteInfographicItemView)

urlpatterns = patterns(
    'infographic.views',
    (r'^edit/(?P<pk>\d+)/$', EditInfographicView.as_view(), {},
     'edit-infographic'),
    url(r'item/add/$', CreateInfographicItemView.as_view(), name='infographicitem_add'),
    url(r'item/(?P<pk>[0-9]+)/$', 
        UpdateInfographicItemView.as_view(), name='infographicitem_update'),
    url(r'item/(?P<pk>[0-9]+)/delete/$', 
        DeleteInfographicItemView.as_view(), name='infographicitem_delete'),)
