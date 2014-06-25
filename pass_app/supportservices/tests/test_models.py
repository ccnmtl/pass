from django.test import TestCase
from pass_app.supportservices.models import SupportServiceBlock
from pass_app.supportservices.tests.factories import UserFactory


class SupportServiceBlockTest(TestCase):
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
