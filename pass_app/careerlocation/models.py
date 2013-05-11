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
    ('DS', 'Defend Strategy'),
)

GRID_COLUMNS = 14
GRID_ROWS = 8


class MapLayer(models.Model):
    def __unicode__(self):
        return self.display_name

    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    legend = models.TextField(null=True, blank=True)
    image = models.FileField(
        upload_to="layers/%Y/%m/%d/", null=True, blank=True)
    z_index = models.IntegerField(default=999)
    transparency = models.IntegerField(default=50)


class ActorQuestion(models.Model):
    def __unicode__(self):
        s = ""
        if self.question:
            if len(self.question) > 25:
                s = self.question[:25] + '...'
            else:
                s = self.question
        return s

    class Meta:
        ordering = ['question']

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
    left = models.IntegerField(null=True, blank=True)
    top = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    image = models.FileField(
        upload_to="layers/%Y/%m/%d/", null=True, blank=True)


class ActorResponse(models.Model):
    def __unicode__(self):
        return "%s [%s : %s]" % (self.user.username, self.actor, self.question)

    user = models.ForeignKey(User, related_name="actor_state_user")
    actor = models.ForeignKey(Actor)
    question = models.ForeignKey(ActorQuestion)
    long_response = models.TextField(null=True, blank=True)


class Strategy(models.Model):
    def __unicode__(self):
        return "%s. %s" % (self.ordinal, self.title)

    class Meta:
        ordering = ['ordinal']

    ordinal = models.PositiveIntegerField()
    title = models.CharField(max_length=256)
    summary = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    pdf = models.FileField(
        upload_to="pdf/", null=True, blank=True)
    example = models.URLField(null=True, blank=True)
    question = models.ForeignKey(ActorQuestion, null=True, blank=True)


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
    strategies_viewed = models.ManyToManyField(
        Strategy, null=True, blank=True, related_name="strategies_viewed")
    strategy_selected = models.ForeignKey(
        Strategy, null=True, blank=True, related_name="strategy_selected")
    strategy_responses = models.ManyToManyField(
        ActorResponse, null=True, blank=True,
        related_name="strategy_responses")

    def get_response(self, question):
        a = self.responses.filter(question=question)
        if len(a) > 0 and len(a[0].long_response) > 0:
            return a[0].long_response

    def grid_cell(self):
        if (self.practice_location_row is None or
                self.practice_location_column is None):
            return None

        return ((self.practice_location_row * GRID_COLUMNS) +
                (self.practice_location_column + 1))


class CareerLocationBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "careerlocation/interview.html"
    js_template_file = "careerlocation/interview_js.html"
    css_template_file = "careerlocation/careerlocation_css.html"
    base_layer = models.ForeignKey(MapLayer)
    optional_layers = models.ManyToManyField(MapLayer,
                                             related_name="optional_layers")
    display_name = "Career Location Exercise"

    view = models.CharField(max_length=2, choices=VIEW_CHOICES)

    max_stakeholders = [0] * 4
    stakeholders = Actor.objects.filter(type="IV")
    boardmembers = Actor.objects.filter(type="BD").order_by("?")

    grid_columns = [0] * GRID_COLUMNS
    grid_rows = [0] * GRID_ROWS

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

        stakeholders = state.actors.filter(
            id__in=[s.id for s in self.stakeholders])
        if len(stakeholders) < 4:
            return False

        for actor in stakeholders:
            r = state.responses.filter(actor=actor)
            if len(r) < 3:
                return False

        if self.view == "LC" or self.view == "BD":
            if state.practice_location_row is None or \
                    state.practice_location_column is None:
                return False

        if self.view == "BD":
            boardmembers = state.actors.filter(
                id__in=[b.id for b in self.boardmembers])
            if len(boardmembers) < 6:
                return False

            for actor in boardmembers:
                r = state.responses.filter(actor=actor)

                if len(r) > 0 and len(r[0].long_response) < 1:
                    return False

        return True

    def layers(self):
        return self.optional_layers.all()

    def practice_location_report(self):
        cells = [0] * (len(self.grid_columns) * len(self.grid_rows))

        for state in CareerLocationState.objects.all():
            grid_cell = state.grid_cell()
            if grid_cell:
                cells[grid_cell - 1] += 1

        return cells

    def actors(self):
        return Actor.objects.filter(type=self.view)


class CareerLocationBlockForm(forms.ModelForm):
    class Meta:
        model = CareerLocationBlock


class CareerLocationSummaryBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "careerlocation/summary.html"
    css_template_file = "careerlocation/careerlocation_css.html"
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
        form = CareerLocationSummaryBlockForm(
            data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True


class CareerLocationSummaryBlockForm(forms.ModelForm):
    class Meta:
        model = CareerLocationSummaryBlock


STRATEGY_VIEW_CHOICES = (
    ('VS', 'View Strategies'),
    ('SS', 'Select Strategy'),
    ('DS', 'Defend Strategy Selection'),
    ('PC', 'Strategy Pros And Cons'),
    ('RS', 'Rethink Strategy Selection'),
)


class CareerLocationStrategyBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "careerlocation/strategy.html"
    js_template_file = "careerlocation/strategy_js.html"
    css_template_file = "careerlocation/careerlocation_css.html"
    base_layer = models.ForeignKey(MapLayer)
    optional_layers = models.ManyToManyField(
        MapLayer, related_name="strategy_optional_layers")
    view = models.CharField(max_length=2, choices=STRATEGY_VIEW_CHOICES)
    questioner = models.ForeignKey(Actor, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)

    display_name = "Career Location Strategy Exercise"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return CareerLocationStrategyBlockForm()

    def edit_form(self):
        return CareerLocationStrategyBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = CareerLocationStrategyBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = CareerLocationStrategyBlockForm(data=vals,
                                               files=files,
                                               instance=self)
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

        if len(state.strategies_viewed.all()) < len(self.strategies()):
            return False

        if self.view != "VS":
            if state.strategy_selected is None:
                return False

        if self.view == 'DS':
            if len(state.strategy_responses.all()) < len(self.questions()):
                return False

        return True

    def strategies(self):
        return Strategy.objects.all().order_by('ordinal')

    def layers(self):
        return self.optional_layers.all()

    def questions(self):
        return self.questioner.questions.all() if self.questioner else None


class CareerLocationStrategyBlockForm(forms.ModelForm):
    class Meta:
        model = CareerLocationStrategyBlock
