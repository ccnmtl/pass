from django.db import models
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms
from django.contrib.auth.models import User

VIEW_CHOICES = (
    ('IV', 'Interview Stakeholders'),
    ('LC', 'Select Practice Location'),
    ('BD', 'Complete Board Application'),
    ('RP', 'Practice Location Report'),
    )

class MapLayer(models.Model):
    def __unicode__(self):
        return self.display_name

    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    legend = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="layers/%Y/%m/%d/", null=True, blank=True)
    z_index = models.IntegerField(default=999);
    transparency = models.IntegerField(default=50);

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
    title = models.CharField(max_length=255, null=True, blank=True)
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

class CareerLocationBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "careerlocation/interview.html"
    js_template_file = "careerlocation/interview_js.html"
    css_template_file = "careerlocation/interview_css.html"
    base_layer = models.ForeignKey(MapLayer)
    display_name = "Career Location Exercise"

    view = models.CharField(max_length=2, choices=VIEW_CHOICES)

    max_stakeholders = [0] * 4
    stakeholders = Actor.objects.filter(type="IV")
    boardmembers = Actor.objects.filter(type="BD").order_by("?")

    grid_columns = [0] * 14
    grid_rows = [0] * 8

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

        state = a[0]

        stakeholders = state.actors.filter(id__in = [s.id for s in self.stakeholders])
        if len(stakeholders) < 4:
            return False

        for actor in stakeholders:
            r = state.responses.filter(actor=actor);
            if len(r) < 3:
                return False

        if self.view == "LC" or self.view == "BD":
            if state.practice_location_row == None or \
               state.practice_location_column == None:
                return False

        if self.view == "BD":
            boardmembers = state.actors.filter(id__in = [b.id for b in self.boardmembers])
            if len(boardmembers) < 6:
                return False

            for actor in boardmembers:
                r = state.responses.filter(actor=actor);

                if len(r) > 0 and len(r[0].long_response) < 1:
                    return False

        return True

    def layers(self):
        return MapLayer.objects.exclude(name="base");

    def practice_location_report(self):
        cells = [0] * (len(self.grid_columns) * len(self.grid_rows))

        for state in CareerLocationState.objects.all():
            grid_cell = state.grid_cell()
            if grid_cell:
                cells[grid_cell - 1] += 1

        return cells

class CareerLocationBlockForm(forms.ModelForm):
    class Meta:
        model = CareerLocationBlock

class CareerLocationState(models.Model):
    def __unicode__(self):
        return self.user.username

    user = models.ForeignKey(User, related_name="career_location_state")
    layers = models.ManyToManyField(MapLayer, null=True, blank=True)
    actors = models.ManyToManyField(Actor, null=True, blank=True)
    responses = models.ManyToManyField(ActorResponse, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    practice_location_row = models.IntegerField(null=True, blank=True)
    practice_location_column = models.IntegerField(null=True, blank=True)

    def get_response(self, question):
        a = self.responses.filter(question=question)
        if len(a) > 0 and len(a[0].long_response) > 0:
            return a[0].long_response

    def grid_cell(self):
        if self.practice_location_row == None or self.practice_location_column == None:
            return None

        columns = len(CareerLocationBlock.grid_columns)
        return (self.practice_location_row * columns) + (self.practice_location_column + 1)


class CareerLocationSummaryBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "careerlocation/summary.html"
    css_template_file = "careerlocation/interview_css.html"
    display_name = "Career Location Summary"

    def boardmembers(self):
        return Actor.objects.filter(type="BD").order_by("order")

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return CareerLocationSummaryBlockForm()

    def edit_form(self):
        return CareerLocationSummaryBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = CareerLocationSummaryBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = CareerLocationSummaryBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class CareerLocationSummaryBlockForm(forms.ModelForm):
    class Meta:
        model = CareerLocationSummaryBlock
