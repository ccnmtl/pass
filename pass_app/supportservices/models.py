from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from pagetree.models import PageBlock


class SupportServiceCategory(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class SupportService(models.Model):
    title = models.TextField()
    phone = models.CharField(max_length=64)
    category = models.ForeignKey(SupportServiceCategory)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class SupportServiceBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "supportservices/list.html"
    js_template_file = "supportservices/list_js.html"
    css_template_file = "supportservices/list_css.html"

    display_name = "Support Services View"

    allow_redo = False

    def services(self):
        return SupportService.objects.all().order_by('category__name', 'title')

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
            state = SupportServiceState.objects.get(user=user)
            state.delete()
        except SupportServiceState.DoesNotExist:
            pass  # calling reset before they've done anything

    @classmethod
    def add_form(self):
        return SupportServiceBlockForm()

    def edit_form(self):
        return SupportServiceBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = SupportServiceBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = SupportServiceBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class SupportServiceBlockForm(forms.ModelForm):
    class Meta:
        model = SupportServiceBlock
        exclude = []


class SupportServiceState(models.Model):
    user = models.ForeignKey(User, related_name="support_service_state")
    services = models.ManyToManyField(SupportService, blank=True)

    def __unicode__(self):
        return self.user.username
