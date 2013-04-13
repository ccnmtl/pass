from django.contrib.auth.models import User
from pass_app.careerlocation.models import Actor, ActorQuestion, \
    ActorResponse, CareerLocationState, MapLayer
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

    class Meta:
        queryset = CareerLocationState.objects.all()
        resource_name = 'career_location_state'
        authorization = UserAuthorization()
        allowed_methods = ['get', 'put', 'post']
