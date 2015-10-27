from pass_app.specialneeds.models import SpecialNeedsCall, \
    SpecialNeedsCallState
import factory
from pagetree.tests.factories import UserFactory


class SpecialNeedsCallFactory(factory.DjangoModelFactory):
    class Meta:
        model = SpecialNeedsCall
    question = factory.Sequence(lambda n: "question%03d" % n)
    answer = factory.Sequence(lambda n: "answer%03d" % n)


class SpecialNeedsCallStateFactory(factory.DjangoModelFactory):
    class Meta:
        model = SpecialNeedsCallState
    user = factory.SubFactory(UserFactory)
