from pass_app.api import UserResource, UserAuthorization
from pass_app.supportservices.models import SupportServiceCategory, \
    SupportService, SupportServiceState
from tastypie import fields
from tastypie.resources import ModelResource


class SupportServiceCategoryResource(ModelResource):
    class Meta:
        queryset = SupportServiceCategory.objects.all()
        resource_name = 'category'
        allowed_methods = ['get']


class SupportServiceResource(ModelResource):
    category = fields.ForeignKey(SupportServiceCategoryResource,
                                 'category', full=True)

    class Meta:
        queryset = SupportService.objects.all()
        resource_name = 'service'
        allowed_methods = ['get']


class SupportServiceStateResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    services = fields.ManyToManyField(
        'pass_app.supportservices.api.SupportServiceResource',
        'services', full=True)

    class Meta:
        queryset = SupportServiceState.objects.all()
        resource_name = 'support_service_state'
        authorization = UserAuthorization()
        allowed_methods = ['get', 'put', 'post']
