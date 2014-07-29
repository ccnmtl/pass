from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from pagetree.models import PageBlock


class InfographicBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "infographic/infographic.html"
    js_template_file = "infographic/infographic_js.html"
    css_template_file = "infographic/infographic_css.html"
    display_name = "Infographic"
    intro_text = models.TextField(default='')

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return InfographicForm()

    def edit_form(self):
        form = InfographicForm(instance=self)
        alt = "<a href='/_infographic/%s/'>Manage Items</a>" % self.id
        form.alt_text = alt
        return form

    @classmethod
    def create(self, request):
        form = InfographicForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = InfographicForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class InfographicItem(models.Model):
    label_name = models.CharField(max_length=64, default='')
    label = models.CharField(max_length=64)
    content = models.TextField()
    map_area_shape = models.CharField(max_length=64, default='')
    coordinates = models.TextField()
    infographic = models.ForeignKey(InfographicBlock)

    def __unicode__(self):
        return self.label_name


class InfographicItemForm(forms.ModelForm):
    class Meta:
        model = InfographicItem

    def __init__(self, *args, **kwargs):
        super(InfographicItemForm, self).__init__(*args, **kwargs)
        # hides the select dropdown
        self.fields['infographic'].widget.attrs['style'] = "display: none"
        # hides the label
        self.fields['infographic'].widget.is_hidden = True


class InfographicForm(forms.ModelForm):
    class Meta:
        model = InfographicBlock


class InfographicState(models.Model):
    user = models.ForeignKey(User, related_name="infographic_state")
    items = models.ManyToManyField(InfographicItem, null=True, blank=True)

    def __unicode__(self):
        return self.user.username
