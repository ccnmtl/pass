from django.db import models
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from django.contrib.auth.models import User

VIEW_CHOICES = (
    ('IV', 'Interview Stakeholders'),
    ('LOC', 'Select Practice Location'),
    ('BD', 'Complete Board Application'),
    )

class MapLayer(models.Model):
    def __unicode__(self):
        return self.display_name

    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    legend = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="layers/%Y/%m/%d/", null=True, blank=True)

class ActorQuestion(models.Model):
    def __unicode__(self):
        return self.question[:25] + '...' if self.question and len(self.question) > 25 else self.question

    question = models.TextField()
    answer = models.TextField(null=True, blank=True)

class Actor(models.Model):
    def __unicode__(self):
        d = dict(VIEW_CHOICES)
        return d[self.type] + ': ' + self.name

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=VIEW_CHOICES)
    profile = models.TextField(null=True, blank=True)
    questions = models.ManyToManyField(ActorQuestion, null=True, blank=True)
    left = models.IntegerField(null=True, blank=True);
    top = models.IntegerField(null=True, blank=True);
    order = models.IntegerField(null=True, blank=True);
    image = models.FileField(upload_to="layers/%Y/%m/%d/", null=True, blank=True)

class ActorResponse(models.Model):
    def __unicode__(self):
        return "%s [%s : %s]" % (self.user.username, self.actor, self.question)

    user = models.ForeignKey(User, related_name="actor_state_user")
    actor = models.ForeignKey(Actor)
    question = models.ForeignKey(ActorQuestion)
    long_response = models.TextField(null=True, blank=True)


class CareerLocationState(models.Model):
    def __unicode__(self):
        return self.user.username

    user = models.ForeignKey(User, related_name="career_location_state")
    layers = models.ManyToManyField(MapLayer, null=True, blank=True)
    actors = models.ManyToManyField(Actor, null=True, blank=True)
    responses = models.ManyToManyField(ActorResponse, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    # practice_location - tbd

class CareerLocationBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "careerlocation/interview.html"
    js_template_file = "careerlocation/interview_js.html"
    css_template_file = "careerlocation/interview_css.html"
    display_name = "Activity: Interview Local Dentists"
    base_layer = models.ForeignKey(MapLayer)

    view = models.CharField(max_length=2, choices=VIEW_CHOICES)

    max_stakeholders = [0] * 4
    stakeholders = Actor.objects.filter(type="IV");
    boardmembers = Actor.objects.filter(type="BD");

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return CareerLocationBlockForm()

    def edit_form(self):
        return CareerLocationBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = CareerLocationBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = CareerLocationBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        '''
            This module is unlocked if:
                The user has selected 4 stakeholders

        '''

        a = CareerLocationState.objects.filter(user=user)
        if len(a) < 1:
            return False

        if len(a[0].actors.all()) < 4:
            return False

        for actor in a[0].actors.all():
            r = a[0].responses.filter(actor=actor);
            if len(r) < 3:
                return False

        return True

    def layers(self):
        return MapLayer.objects.exclude(name="base");

class CareerLocationBlockForm(forms.ModelForm):
    class Meta:
        model = CareerLocationBlock


