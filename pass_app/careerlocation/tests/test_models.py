from django.test import TestCase
from django.contrib.auth.models import User
from pass_app.careerlocation.models import MapLayer, ActorQuestion
from pass_app.careerlocation.models import Actor, ActorResponse
from pass_app.careerlocation.models import Strategy


class MapLayerTest(TestCase):
    def test_unicode(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        self.assertEqual(str(m), "test display name")


class ActorQuestionTest(TestCase):
    def test_unicode(self):
        aq = ActorQuestion.objects.create(question="short question")
        self.assertEqual(str(aq), "short question")
        aq.question = ''.join(str(x) for x in range(25))
        self.assertEqual(str(aq), "0123456789101112131415161...")


class ActorTest(TestCase):
    def test_unicode(self):
        a = Actor.objects.create(name="test actor", type="IV")
        self.assertEqual(str(a), "Interview Stakeholders: test actor")


class ActorResponseTest(TestCase):
    def test_unicode(self):
        u = User.objects.create(username="testuser")
        a = Actor.objects.create(name="test actor", type="IV")
        aq = ActorQuestion.objects.create(question="short question")
        ar = ActorResponse.objects.create(actor=a, user=u, question=aq)
        self.assertEqual(
            str(ar),
            "testuser [Interview Stakeholders: test actor : short question]"
        )


class StrategyTest(TestCase):
    def test_unicode(self):
        s = Strategy.objects.create(ordinal=1, title="test strategy")
        self.assertEqual(str(s), "1. test strategy")
