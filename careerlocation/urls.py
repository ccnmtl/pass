from django.conf.urls.defaults import *
import os.path
from tastypie.api import Api
from careerlocation.api import *

media_root = os.path.join(os.path.dirname(__file__),"media")

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(MapLayerResource())
v1_api.register(ActorQuestionResource())
v1_api.register(ActorResource())
v1_api.register(ActorResponseResource())
v1_api.register(CareerLocationStateResource())

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
    (r'^api/', include(v1_api.urls))
)