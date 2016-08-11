from .views import CreateInfographicItemView, UpdateInfographicItemView, \
    DeleteInfographicItemView, InfographicDetailView, SaveInfographicState
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', InfographicDetailView.as_view(), {},
        'infographic-detail'),
    url(r'^(?P<pk>\d+)/add/item/$', CreateInfographicItemView.as_view(), {},
        'infographicitem-add'),
    url(r'^edit/item/(?P<pk>[0-9]+)/$', UpdateInfographicItemView.as_view(),
        {}, 'infographicitem-update'),
    url(r'^delete/item/(?P<pk>[0-9]+)/$', DeleteInfographicItemView.as_view(),
        {}, 'infographicitem-delete'),
    url(r'^save/item/$', SaveInfographicState.as_view(), {},
        'infographicitem-save'),
]
