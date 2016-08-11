from .views import SpecialNeedsSaveStateView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^save/item/$', login_required(SpecialNeedsSaveStateView.as_view()),
        {}, 'phonecallstate-save'),
]
