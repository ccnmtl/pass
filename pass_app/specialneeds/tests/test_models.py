from django.test import TestCase
from pass_app.specialneeds.models import SpecialNeedsCallBlock, \
    SpecialNeedsCall
from pass_app.specialneeds.tests.factories import \
    SpecialNeedsCallFactory, SpecialNeedsCallStateFactory
from pagetree.tests.factories import UserFactory


class SpecialNeedsCallBlockTest(TestCase):
    def setUp(self):
        for i in range(5):
            SpecialNeedsCallFactory()

    def test_needs_submit(self):
        block = SpecialNeedsCallBlock()
        self.assertFalse(block.needs_submit())

    def test_add_form(self):
        f = SpecialNeedsCallBlock.add_form()
        self.assertEquals(len(f.fields), 0)

    def test_edit_form(self):
        block = SpecialNeedsCallBlock()
        f = block.edit_form()
        self.assertEquals(len(f.fields), 0)

    def test_unlocked(self):
        block = SpecialNeedsCallBlock()
        user = UserFactory()
        self.assertTrue(block.unlocked(user))

    def test_clear_submissions(self):
        state = SpecialNeedsCallStateFactory()
        all = SpecialNeedsCall.objects.all()
        for question in all:
            state.questions.add(question)

        self.assertEquals(state.questions.count(), all.count())

        block = SpecialNeedsCallBlock()
        block.clear_user_submissions(state.user)
        self.assertEquals(state.questions.count(), 0)
