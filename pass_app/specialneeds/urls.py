from .views import SpecialNeedsSaveStateView
from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    'specialneeds.views',
    (r'^save/item/$', login_required(SpecialNeedsSaveStateView.as_view()), {},
     'phonecallstate-save'),)
