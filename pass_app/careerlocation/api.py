from django.contrib.auth.models import User
from pass_app.careerlocation.models import Actor, ActorQuestion, \
    ActorResponse, CareerLocationState, MapLayer, Strategy
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class UsernameAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(username=request.user.username)

        return object_list.none()


class UserAuthorization(Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(user=request.user)

        return object_list.none()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser', 'date_joined']
        allowed_methods = ['get']
        authorization = UsernameAuthorization()


class MapLayerResource(ModelResource):
    class Meta:
        queryset = MapLayer.objects.exclude(name="base")
        resource_name = 'map_layer'
        allowed_methods = ['get']


class ActorQuestionResource(ModelResource):
    class Meta:
        queryset = ActorQuestion.objects.all()
        resource_name = 'actor_question'
        allowed_methods = ['get']


class ActorResource(ModelResource):
    questions = fields.ManyToManyField(
        'pass_app.careerlocation.api.ActorQuestionResource',
        'questions', full=True)

    class Meta:
        queryset = Actor.objects.all()
        resource_name = 'actor'
        allowed_methods = ['get']


class ActorResponseResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    actor = fields.ForeignKey(ActorResource, 'actor', full=True)
    question = fields.ForeignKey(ActorQuestionResource, 'question', full=True)

    class Meta:
        queryset = ActorResponse.objects.all()
        resource_name = 'actor_response'
        authorization = UserAuthorization()
        allowed_methods = ['get', 'put', 'post']


class StrategyResource(ModelResource):
    class Meta:
        queryset = Strategy.objects.all()
        resource_name = 'strategy'
        allowed_methods = ['get']
        excludes = ['pdf', 'example']

    def dehydrate(self, bundle):
        bundle.data['pdf_url'] = ''
        bundle.data['example_url'] = ''
        return bundle


class CareerLocationStateResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    layers = fields.ManyToManyField(
        'pass_app.careerlocation.api.MapLayerResource', 'layers',
        full=True)
    actors = fields.ManyToManyField(
        'pass_app.careerlocation.api.ActorResource', 'actors',
        full=True)
    responses = fields.ManyToManyField(
        'pass_app.careerlocation.api.ActorResponseResource', 'responses',
        full=True)
    strategies_viewed = fields.ManyToManyField(
        'pass_app.careerlocation.api.StrategyResource',
        'strategies_viewed',
        full=True,
        null=True)
    strategy_selected = fields.ForeignKey(StrategyResource,
                                          'strategy_selected',
                                          full=True,
                                          null=True)

    #def hydrate_m2m(self, bundle):
    #    if bundle.data.get("strategies_viewed"):
    #        for sid in bundle.data["strategies_viewed"]:
    #            strategy = Strategy.objects.get(id=sid)
    #            bundle.obj.strategies_viewed.add(strategy)

    class Meta:
        queryset = CareerLocationState.objects.all()
        resource_name = 'career_location_state'
        authorization = UserAuthorization()
        allowed_methods = ['get', 'put', 'post']
