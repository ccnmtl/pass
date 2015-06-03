from django.test import TestCase
from pagetree.tests.factories import UserFactory
from pass_app.specialneeds.tests.factories import \
    SpecialNeedsCallFactory
from pass_app.specialneeds.models import \
    SpecialNeedsCallState
from django.core.urlresolvers import reverse


class SpecialNeedsViewTest(TestCase):

    def setUp(self):
        self.question1 = SpecialNeedsCallFactory()
        self.question2 = SpecialNeedsCallFactory()
        self.user = UserFactory()

    def test_anonymous_user(self):
        response = self.client.get(reverse('phonecallstate-save'))
        self.assertEquals(response.status_code, 302)

    def test_logged_in_user_get(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password="test"))
        response = self.client.get(reverse('phonecallstate-save'))
        self.assertEquals(response.status_code, 405)

    def test_logged_in_user_post_fail(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password="test"))
        response = self.client.post(
            reverse('phonecallstate-save'),
            {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 404)

    def test_logged_in_user_post_success(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password="test"))
        response = self.client.post(
            reverse('phonecallstate-save'),
            {'item_id': self.question1.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        state = SpecialNeedsCallState.objects.get(user=self.user)
        self.assertTrue(self.question1 in state.questions.all())
