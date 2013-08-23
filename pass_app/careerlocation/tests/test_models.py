from django.test import TestCase
from django.contrib.auth.models import User
from pass_app.careerlocation.models import MapLayer, ActorQuestion
from pass_app.careerlocation.models import Actor, ActorResponse
from pass_app.careerlocation.models import Strategy, CareerLocationState
from pass_app.careerlocation.models import CareerLocationBlock


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
        aq.question = None
        self.assertEqual(str(aq), "")


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


class CareerLocationStateTest(TestCase):
    def test_unicode(self):
        u = User.objects.create(username="testuser")
        cls = CareerLocationState.objects.create(user=u)
        self.assertEqual(str(cls), "testuser")

    def test_get_response(self):
        u = User.objects.create(username="testuser")
        a = Actor.objects.create(name="test actor", type="IV")
        aq = ActorQuestion.objects.create(question="short question")
        ar = ActorResponse.objects.create(actor=a, user=u, question=aq,
                                          long_response="a long response")
        cls = CareerLocationState.objects.create(user=u)
        self.assertEqual(cls.get_response(aq), None)
        cls.responses.add(ar)
        self.assertEqual(cls.get_response(aq), "a long response")

    def test_grid_cell(self):
        u = User.objects.create(username="testuser")
        cls = CareerLocationState.objects.create(user=u)
        self.assertEqual(cls.grid_cell(), None)
        cls.practice_location_row = 0
        cls.practice_location_column = 0
        self.assertEqual(cls.grid_cell(), 1)


class CareerLocationBlockTest(TestCase):
    def test_needs_submit(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        clb = CareerLocationBlock.objects.create(base_layer=m, view='IV')
        self.assertFalse(clb.needs_submit())

    def test_add_form(self):
        f = CareerLocationBlock.add_form()
        self.assertTrue('view' in f.fields)

    def test_edit_form(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        clb = CareerLocationBlock.objects.create(base_layer=m, view='IV')
        f = clb.edit_form()
        self.assertTrue('view' in f.fields)

    def test_unlocked(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        clb = CareerLocationBlock.objects.create(base_layer=m, view='IV')
        u = User.objects.create(username="testuser")
        # with no state, it shouldn't be unlocked yet
        self.assertFalse(clb.unlocked(u))
        # with a state, but no stakeholders
        cls = CareerLocationState.objects.create(user=u)
        self.assertFalse(clb.unlocked(u))
        actors = [
            Actor.objects.create(name="test actor 1", type="IV"),
            Actor.objects.create(name="test actor 2", type="IV"),
            Actor.objects.create(name="test actor 3", type="IV"),
            Actor.objects.create(name="test actor 4", type="IV")]
        for a in actors:
            cls.actors.add(a)

        # we have enough stakeholders now, but no responses to them
        self.assertFalse(clb.unlocked(u))
        aq = ActorQuestion.objects.create(question="short question")
        for a in actors:
            # need at least three responses for each actor
            for _ in range(3):
                ar = ActorResponse.objects.create(actor=a, user=u, question=aq)
                cls.responses.add(ar)
        # finally, that should unlock it
        self.assertTrue(clb.unlocked(u))

    def test_layers(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        clb = CareerLocationBlock.objects.create(base_layer=m, view='IV')
        self.assertEqual(list(clb.layers()), [])

    def test_actors(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        clb = CareerLocationBlock.objects.create(base_layer=m, view='IV')
        self.assertEqual(list(clb.actors()), [])

    def test_practice_location_report(self):
        m = MapLayer.objects.create(
            name="test name", display_name="test display name")
        clb = CareerLocationBlock.objects.create(base_layer=m, view='IV')
        self.assertEqual(clb.practice_location_report(), [0] * 112)
