import factory
from pagetree.tests.factories import UserFactory

from pass_app.supportservices.models import SupportServiceCategory, \
    SupportService, SupportServiceState


class SupportServiceCategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = SupportServiceCategory
    name = factory.Sequence(lambda n: "category%03d" % n)


class SupportServiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = SupportService
    title = factory.Sequence(lambda n: "service%03d" % n)
    phone = "555-212-1111"
    category = factory.SubFactory(SupportServiceCategoryFactory)
    description = "description"


class SupportServiceStateFactory(factory.DjangoModelFactory):
    class Meta:
        model = SupportServiceState
    user = factory.SubFactory(UserFactory)
