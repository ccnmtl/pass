from django import forms
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

    def get_services(self):
        return SupportService.objects.all().order_by('category__name', 'title')

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

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

    def unlocked(self, user):
        return True


class SupportServiceBlockForm(forms.ModelForm):
    class Meta:
        model = SupportServiceBlock
