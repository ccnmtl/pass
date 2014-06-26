from django.test import TestCase
from pass_app.supportservices.models import SupportServiceBlock, \
    SupportService
from pass_app.supportservices.tests.factories import SupportServiceFactory, \
    SupportServiceStateFactory


class SupportServiceBlockTest(TestCase):
    def setUp(self):
        for i in range(5):
            SupportServiceFactory()

    def test_needs_submit(self):
        block = SupportServiceBlock()
        self.assertTrue(block.needs_submit())

    def test_add_form(self):
        f = SupportServiceBlock.add_form()
        self.assertEquals(len(f.fields), 0)

    def test_edit_form(self):
        block = SupportServiceBlock()
        f = block.edit_form()
        self.assertEquals(len(f.fields), 0)

    def test_unlocked(self):
        block = SupportServiceBlock()
        state = SupportServiceStateFactory()
        self.assertFalse(block.unlocked(state.user))

        for service in SupportService.objects.all():
            state.services.add(service)
        self.assertTrue(block.unlocked(state.user))

        block.clear_user_submissions(state.user)
        self.assertFalse(block.unlocked(state.user))
