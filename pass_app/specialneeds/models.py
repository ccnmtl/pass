from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from pagetree.models import PageBlock


class SpecialNeedsCall(models.Model):
    question = models.TextField()
    answer = models.TextField()
    ordinality = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.question

    class Meta:
        ordering = ('ordinality', 'id')


class SpecialNeedsCallBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "specialneeds/phonecall.html"
    js_template_file = "specialneeds/phonecall_js.html"
    css_template_file = "specialneeds/phonecall_css.html"

    display_name = "Special Needs Call View"

    allow_redo = False

    def questions(self):
        return SpecialNeedsCall.objects.all()

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    def unlocked(self, user):
        return True

    def clear_user_submissions(self, user):
        try:
            state = SpecialNeedsCallState.objects.get(user=user)
            state.delete()
        except SpecialNeedsCallState.DoesNotExist:
            pass  # calling reset before they've done anything

    @classmethod
    def add_form(self):
        return SpecialNeedsCallBlockForm()

    def edit_form(self):
        return SpecialNeedsCallBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = SpecialNeedsCallBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = SpecialNeedsCallBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class SpecialNeedsCallBlockForm(forms.ModelForm):
    class Meta:
        model = SpecialNeedsCallBlock


class SpecialNeedsCallState(models.Model):
    user = models.ForeignKey(User, related_name="special_needs_call")
    questions = models.ManyToManyField(SpecialNeedsCall, null=True, blank=True)

    def __unicode__(self):
        return self.user.username
