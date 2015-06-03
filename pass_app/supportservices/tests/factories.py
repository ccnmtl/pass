import factory
from pagetree.tests.factories import UserFactory

from pass_app.supportservices.models import SupportServiceCategory, \
    SupportService, SupportServiceState


class SupportServiceCategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SupportServiceCategory
    name = factory.Sequence(lambda n: "category%03d" % n)


class SupportServiceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SupportService
    title = factory.Sequence(lambda n: "service%03d" % n)
    phone = "555-212-1111"
    category = factory.SubFactory(SupportServiceCategoryFactory)
    description = "description"


class SupportServiceStateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SupportServiceState
    user = factory.SubFactory(UserFactory)
