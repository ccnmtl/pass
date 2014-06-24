from django.conf.urls.defaults import include, patterns
from pass_app.supportservices.api import SupportServiceCategoryResource, \
    SupportServiceResource
from tastypie.api import Api
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

v1_api = Api(api_name='v1')
v1_api.register(SupportServiceCategoryResource())
v1_api.register(SupportServiceResource())

urlpatterns = patterns(
    '',
    (r'^api/', include(v1_api.urls))
)
