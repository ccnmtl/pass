from pass_app.supportservices.models import SupportServiceCategory, \
    SupportService
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
