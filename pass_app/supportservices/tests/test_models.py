from django.test import TestCase
from pagetree.tests.factories import UserFactory

from pass_app.supportservices.models import SupportServiceBlock, SupportService
from pass_app.supportservices.tests.factories import SupportServiceFactory, \
    SupportServiceStateFactory


class SupportServiceTest(TestCase):

    def test_unicode(self):
        service = SupportServiceFactory(title="test")
        self.assertEquals(service.__unicode__(), "test")


class SupportServiceBlockTest(TestCase):

    def setUp(self):
        for i in range(5):
            SupportServiceFactory()

    def test_services(self):
        block = SupportServiceBlock()
        self.assertEquals(block.services().count(), 5)

    def test_needs_submit(self):
        block = SupportServiceBlock()
        self.assertFalse(block.needs_submit())

    def test_add_form(self):
        f = SupportServiceBlock.add_form()
        self.assertEquals(len(f.fields), 0)

    def test_edit_form(self):
        block = SupportServiceBlock()
        f = block.edit_form()
        self.assertEquals(len(f.fields), 0)

    def test_unlocked(self):
        block = SupportServiceBlock()
        user = UserFactory()
        self.assertTrue(block.unlocked(user))

    def test_clear_submissions(self):
        state = SupportServiceStateFactory()
        all_services = SupportService.objects.all()
        for service in all_services:
            state.services.add(service)

        self.assertEquals(state.services.count(), all_services.count())

        block = SupportServiceBlock()
        block.clear_user_submissions(state.user)
        self.assertEquals(state.services.count(), 0)
