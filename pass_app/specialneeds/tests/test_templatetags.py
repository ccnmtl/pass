from django.test import TestCase
from pass_app.specialneeds.models import SpecialNeedsCallState
from pass_app.specialneeds.tests.factories import \
    SpecialNeedsCallFactory
from pagetree.tests.factories import UserFactory
from pass_app.specialneeds.templatetags.phonecallstate \
    import get_user_state


class PhoneCallTagTest(TestCase):
    def setUp(self):
        self.question1 = SpecialNeedsCallFactory()
        self.question2 = SpecialNeedsCallFactory()
        self.user = UserFactory()

    def test_user_no_state(self):
        context = {'user': self.user}
        self.assertFalse(get_user_state(context, self.question1))

    def test_user_partial_state(self):
        context = {'user': self.user}
        state = SpecialNeedsCallState.objects.create(user=self.user)
        self.assertFalse(get_user_state(context, self.question1))

        state.questions.add(self.question2)
        self.assertFalse(get_user_state(context, self.question1))

    def test_user_full_state(self):
        context = {'user': self.user}
        state = SpecialNeedsCallState.objects.create(user=self.user)
        state.questions.add(self.question1)
        self.assertTrue(get_user_state(context, self.question1))

        state.questions.add(self.question2)
        self.assertTrue(get_user_state(context, self.question1))
