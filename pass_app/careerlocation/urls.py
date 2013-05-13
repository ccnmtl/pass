from django.conf.urls.defaults import include, patterns
from pass_app.careerlocation.api import ActorResource, ActorResponseResource, \
    ActorQuestionResource, CareerLocationStateResource, MapLayerResource, \
    UserResource, StrategyResource
from tastypie.api import Api
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(MapLayerResource())
v1_api.register(ActorQuestionResource())
v1_api.register(ActorResource())
v1_api.register(ActorResponseResource())
v1_api.register(CareerLocationStateResource())
v1_api.register(StrategyResource())

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'^api/', include(v1_api.urls))
)