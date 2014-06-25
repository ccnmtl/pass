from pass_app.api import UserResource, UserAuthorization
from pass_app.careerlocation.models import Actor, ActorQuestion, \
    ActorResponse, CareerLocationState, MapLayer, Strategy
from tastypie import fields
from tastypie.resources import ModelResource


class MapLayerResource(ModelResource):
    class Meta:
        queryset = MapLayer.objects.exclude(name="base")
        resource_name = 'map_layer'
        allowed_methods = ['get']

    def dehydrate(self, bundle):
        for key, value in bundle.data.items():
            bundle.data[key] = str(bundle.data[key])

        return bundle

    def render_list(self, request, lst):
        data = []
        for user in lst:
            bundle = self.build_bundle(obj=user, request=request)
            dehydrated = self.full_dehydrate(bundle)
            data.append(dehydrated.data)
        return data


class ActorQuestionResource(ModelResource):
    class Meta:
        queryset = ActorQuestion.objects.all()
        resource_name = 'actor_question'
        allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['question'] = str(bundle.data['question'])
        bundle.data['answer'] = str(bundle.data['answer'])
        bundle.data['id'] = str(bundle.data['id'])
        return bundle


class ActorResource(ModelResource):
    questions = fields.ManyToManyField(
        'pass_app.careerlocation.api.ActorQuestionResource',
        'questions', full=True)

    def dehydrate(self, bundle):
        return bundle

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
    question = fields.ForeignKey(ActorQuestionResource, 'question', full=True)

    class Meta:
        queryset = Strategy.objects.all()
        resource_name = 'strategy'
        allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle = super(ModelResource, self).dehydrate(bundle)
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
    strategy_responses = fields.ManyToManyField(
        'pass_app.careerlocation.api.ActorResponseResource',
        'strategy_responses',
        full=True,
        null=True)

    class Meta:
        queryset = CareerLocationState.objects.all()
        resource_name = 'career_location_state'
        authorization = UserAuthorization()
        allowed_methods = ['get', 'put', 'post']
