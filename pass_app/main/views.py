from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_str
from pagetree.helpers import get_hierarchy, get_section_from_path, \
    get_module, needs_submit, submitted
from pagetree.models import Hierarchy
from pagetree_export.exportimport import export_zip, import_zip
from pass_app.careerlocation.models import Actor, CareerLocationState, \
    ActorResponse, Strategy
from pass_app.main.models import UserProfile, UserVisited
from pass_app.supportservices.models import SupportServiceState
from quizblock.models import Submission, Response
from zipfile import ZipFile
import csv
import django.core.exceptions
import os


def get_or_create_profile(user, section):
    if user.is_anonymous():
        return None
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
    except django.core.exceptions.MultipleObjectsReturned:
        user_profile = UserProfile.objects.filter(user=user)[0]
        created = False
    if created:
        first_leaf = section.hierarchy.get_first_leaf(section)
        ancestors = first_leaf.get_ancestors()
        for a in ancestors:
            user_profile.save_visit(a)
    return user_profile


def _unlocked(profile, section):
    """ if the user can proceed past this section """
    if profile is None:
        return False
    if not section or section.is_root() or profile.has_visited(section):
        return True

    previous = section.get_previous()
    if not previous:
        return True
    if not profile.has_visited(previous):
        return False

    # if the previous page had blocks to submit
    # we only let them by if they submitted
    for p in previous.pageblock_set.all():
        if hasattr(p.block(), 'unlocked'):
            if not p.block().unlocked(profile.user):
                return False

    return profile.has_visited(previous)


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if isinstance(items, type({})):
                ctx = RequestContext(request)
                return render_to_response(self.template_name,
                                          items,
                                          context_instance=ctx)
            else:
                return items
        return rendered_func


def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all(
    ) if hasattr(p.block(), 'needs_submit') and p.block().needs_submit()]
    return quizzes != []


def allow_redo(section):
    """ if blocks on the page allow redo """
    allowed = True
    for p in section.pageblock_set.all():
        if hasattr(p.block(), 'allow_redo'):
            if not p.block().allow_redo:
                allowed = False
    return allowed


@login_required
@rendered_with('main/intro.html')
def intro(request):
    return {
        'demographic_survey_complete': demographic_survey_complete(request)
    }


@login_required
@rendered_with('main/page.html')
def demographic(request, path):
    hierarchy = get_hierarchy('demographic')
    return process_page(request, path, hierarchy)


@login_required
@rendered_with('main/page.html')
def module_one(request, path):
    if not demographic_survey_complete(request):
        hierarchy = get_hierarchy('demographic')
        return HttpResponseRedirect(hierarchy.get_root().get_absolute_url())

    hierarchy = get_hierarchy('module-one')
    return process_page(request, path, hierarchy)


@login_required
@rendered_with('main/page.html')
def module_two(request, path):
    if not demographic_survey_complete(request):
        hierarchy = get_hierarchy('demographic')
        return HttpResponseRedirect(hierarchy.get_root().get_absolute_url())

    hierarchy = get_hierarchy('module-two')
    return process_page(request, path, hierarchy)


@login_required
@rendered_with('main/page.html')
def module_three(request, path):
    if not demographic_survey_complete(request):
        hierarchy = get_hierarchy('demographic')
        return HttpResponseRedirect(hierarchy.get_root().get_absolute_url())

    hierarchy = get_hierarchy('module-three')
    return process_page(request, path, hierarchy)


@login_required
@rendered_with('main/page.html')
def module_four(request, path):
    if not demographic_survey_complete(request):
        hierarchy = get_hierarchy('demographic')
        return HttpResponseRedirect(hierarchy.get_root().get_absolute_url())

    hierarchy = get_hierarchy('module-four')
    return process_page(request, path, hierarchy)


@login_required
@rendered_with('main/admin_page.html')
def reports(request, path):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    hierarchy = get_hierarchy('reports')
    return process_page(request, path, hierarchy)


@login_required
def process_page(request, path, hierarchy):
    section = get_section_from_path(path, hierarchy=hierarchy)

    root = hierarchy.get_root()
    module = get_module(section)

    user_profile = get_or_create_profile(user=request.user, section=section)
    can_access = _unlocked(user_profile, section)
    if can_access:
        user_profile.save_visit(section)
    else:
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(user_profile.last_location)

    can_edit = False
    if not request.user.is_anonymous():
        can_edit = request.user.is_staff

    if section.id == root.id:
        # trying to visit the root page
        if section.get_first_leaf():
            # just send them to the first child, but save
            # the ancestors first
            first_leaf = section.get_first_leaf()
            ancestors = first_leaf.get_ancestors()
            user_profile.save_visits(ancestors)
            return HttpResponseRedirect(first_leaf.get_absolute_url())

    if request.method == "POST":
        return handle_page_post(request, section, hierarchy, path)
    else:
        instructor_link = has_responses(section)
        allow_next_link = not needs_submit(
            section) or submitted(section, request.user)

        return dict(section=section,
                    module=module,
                    allow_next_link=allow_next_link,
                    needs_submit=needs_submit(section),
                    is_submitted=submitted(section, request.user),
                    modules=root.get_children(),
                    root=section.hierarchy.get_root(),
                    instructor_link=instructor_link,
                    can_edit=can_edit,
                    allow_redo=allow_redo(section),
                    next_unlocked=_unlocked(
                        user_profile, section.get_next())
                    )


def handle_page_post(request, section, hierarchy, path):
    # user has submitted a form. deal with it
    if request.POST.get('action', '') == 'reset':
        section.reset(request.user)
        return HttpResponseRedirect(section.get_absolute_url())

    section.submit(request.POST, request.user)

    if hierarchy.name == 'demographic' and path.startswith("survey"):
        return HttpResponseRedirect("/")

    next_section = section.get_next()
    if next_section:
        # ignoring proceed and always pushing them along. see PMT #77454
        return HttpResponseRedirect(next_section.get_absolute_url())
    else:
        return HttpResponseRedirect("/")


@login_required
@rendered_with("main/instructor_page.html")
def instructor_page(request, path):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    hierarchy_name, slash, section_path = path.partition('/')
    section = get_section_from_path(section_path, hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()

    if request.method == "POST":
        if 'clear' in request.POST.keys():
            submission = get_object_or_404(
                Submission, id=request.POST['clear'])
            submission.delete()
            return HttpResponseRedirect(
                "/instructor" + section.get_absolute_url())

    quizzes = [p.block() for p in section.pageblock_set.all(
    ) if hasattr(p.block(), 'needs_submit') and p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                modules=root.get_children(),
                root=root)


def clean_header(s):
    s = s.replace('<div class=\'question-sub\'>', '')
    s = s.replace('<div class=\'question\'>', '')
    s = s.replace('<div class=\"mf-question\">', '')
    s = s.replace('<div class=\"sw-question\">', '')
    s = s.replace('<p>', '')
    s = s.replace('</p>', '')
    s = s.replace('</div>', '')
    s = s.replace('\n', '')
    s = s.replace('\r', '')
    s = s.replace('<', '')
    s = s.replace('>', '')
    s = s.replace('\'', '')
    s = s.replace('\"', '')
    s = s.replace(',', '')
    s = s.encode('utf-8')
    return s


class Column(object):
    def __init__(self, hierarchy, question=None, answer=None, actor=None,
                 actor_question=None, location=None, notes=None,
                 strategy=None):
        self.hierarchy = hierarchy
        self.question = question
        self.answer = answer
        self.module_name = self.hierarchy.get_top_level()[0].label
        self.actor = actor
        self.actor_question = actor_question
        self.location = location
        self.notes = notes
        self.strategy = strategy

        if self.question:
            self._submission_cache = Submission.objects.filter(
                quiz=self.question.quiz)
            self._response_cache = Response.objects.filter(
                question=self.question)
            self._answer_cache = self.question.answer_set.all()

        if self.actor or self.location or self.notes or self.strategy:
            self._state_cache = CareerLocationState.objects.all()

    def last_visited_id(self):
        return "%s_last_visited" % (self.hierarchy.id)

    def question_id(self):
        return "%s_question_%s" % (self.hierarchy.id, self.question.id)

    def question_answer_id(self):
        return "%s_%s" % (self.question_id(), self.answer.id)

    def actor_id(self):
        if self.actor.type == "IV":
            t = "stakeholder"
            return "%s_%s_%s" % (self.hierarchy.id, t, self.actor.id)
        elif self.actor.type == "BD":
            t = "boardmember"
            return "%s_%s_%s" % (self.hierarchy.id, t, self.actor.id)
        elif self.actor.type == "DS":
            t = "defend_strategy"
            return "%s_%s" % (self.hierarchy.id, t)

    def actor_answer_id(self):
        return "%s_%s" % (self.actor_id(), self.actor_question.id)

    def select_strategy_id(self):
        return "%s_select_strategy" % self.hierarchy.id

    def strategy_question_id(self):
        return "%s_strategy_question_%s" % (self.hierarchy.id,
                                            self.strategy.id)

    def location_id(self):
        return "%s_careerlocation_location" % (self.hierarchy.id)

    def notes_id(self):
        return "%s_careerlocation_notes" % (self.hierarchy.id)

    def last_visited_value(self, user):
        uv = UserVisited.objects.filter(
            user__user=user,
            section__hierarchy=self.hierarchy).order_by("-visited_time")[:1]
        if len(uv) > 0:
            return uv[0].visited_time.strftime("%m/%d/%y %H:%M:%S")
        return ""

    def question_value(self, user):
        r = self._submission_cache.filter(user=user).order_by("-submitted")
        if r.count() == 0:
            # user has not submitted this form
            return ""
        submission = r[0]
        r = self._response_cache.filter(submission=submission)
        if r.count() > 0:
            if (self.question.is_short_text() or
                    self.question.is_long_text()):
                return r[0].value
            elif self.question.is_multiple_choice():
                if self.answer.value in [res.value for res in r]:
                    return self.answer.id
            else:  # single choice
                for a in self._answer_cache:
                    if a.value == r[0].value:
                        return a.id
        return ''

    def cached_user_value(self, user):
        a = self._state_cache.filter(user=user)
        if a.count() == 0:
            return ""

        state = a[0]
        dispatch = [
            (self.strategy and self.actor_question,
             lambda: self.first_strategy_long_response(state)),
            (self.has_actor_question_and_ds(),
             lambda: self.first_actor_strategy_long_response(state)),
            (self.actor and self.actor_question,
             lambda: self.first_actor_question_id(state)),
            (self.actor, lambda: self.first_long_response(state)),
            (self.location, lambda: state.grid_cell()),
            (self.notes, lambda: state.notes),
            (self.strategy and state.strategy_selected is not None,
             lambda: state.strategy_selected)
        ]
        for c, v in dispatch:
            if c:
                return v()
        return ""

    def first_strategy_long_response(self, state):
        responses = state.strategy_responses.filter(
            question=self.actor_question)
        if responses.count() > 0:
            return responses[0].long_response
        return ""

    def first_actor_strategy_long_response(self, state):
        responses = state.strategy_responses.filter(
            actor=self.actor, question=self.actor_question)
        if responses.count() > 0:
            return responses[0].long_response
        return ""

    def first_actor_question_id(self, state):
        responses = state.responses.filter(
            actor=self.actor, question=self.actor_question)
        if responses.count() > 0:
            return self.actor_question.id
        return ""

    def first_long_response(self, state):
        responses = state.responses.filter(actor=self.actor)
        if responses.count() > 0:
            return responses[0].long_response
        return ""

    def has_actor_question_and_ds(self):
        return (self.actor and
                self.actor_question and
                self.actor.type == "DS")

    def user_value(self, user):
        if self.question:
            return self.question_value(user)
        elif not hasattr(self, "_state_cache"):
            return self.last_visited_value(user)
        else:
            return self.cached_user_value(user)

    def make_question_row(self):
        row = [self.question_id(), self.module_name,
               self.question.question_type,
               clean_header(self.question.text)]
        if self.answer:
            row.append(self.answer.id)
            row.append(clean_header(self.answer.label))
        return row

    def key_row(self):
        dispatch = [
            (self.question,
             lambda: self.make_question_row()),
            (self.actor and self.actor.type == "DS",
             lambda: [self.actor_answer_id(), self.module_name, "short text",
                      clean_header(self.actor_question.question)]),
            ((self.actor and hasattr(self.actor, 'questions')
              and len(self.actor.questions.all()) > 1),
             lambda: [self.actor_id(), self.module_name,
                      "multiple choice", clean_header(self.actor.name),
                      self.actor_question.id,
                      clean_header(self.actor_question.question)]),
            ((self.actor and hasattr(self.actor, 'questions')
              and len(self.actor.questions.all()) == 1),
             lambda: [self.actor_id(), self.module_name, "short text",
                      clean_header(self.actor_question.question)]),
            (self.location,
             lambda: [self.location_id(), self.module_name,
                      "grid cell", self.location]),
            (self.notes,
             lambda: [self.notes_id(), self.module_name,
                      "long text", self.notes]),
            (self.strategy and self.actor_question,
             lambda: [self.strategy_question_id(),
                      self.module_name, "short text",
                      clean_header(self.actor_question.question)]),
            (self.strategy,
             lambda: [self.select_strategy_id(), self.module_name,
                      "single choice", "Select a strategy",
                      self.strategy.id,
                      clean_header(self.strategy.title)]),
        ]
        for c, v in dispatch:
            if c:
                return v()
        return [self.last_visited_id(),
                self.module_name,
                "short text",
                "Last Visited Date"]

    def header_column(self):
        conds = [
            (self.question and self.answer, lambda: self.question_answer_id()),
            (self.question, lambda: self.question_id()),
            (self.actor and self.actor_question,
             lambda: self.actor_answer_id()),
            (self.actor, lambda: self.actor_id()),
            (self.location, lambda: self.location_id()),
            (self.notes, lambda: self.notes_id()),
            (self.strategy and self.actor_questions,
             lambda: self.strategy_question_id()),
            (self.strategy, lambda: self.select_strategy_id()),
        ]

        for c, v in conds:
            if c:
                return v()
        return [self.last_visited_id()]


def _get_quiz_key(h, s):
    quiz_type = ContentType.objects.filter(name='quiz')
    columns = []
    # quizzes
    for p in s.pageblock_set.filter(content_type=quiz_type):
        for q in p.block().question_set.all():
            if q.answerable():
                # need to make a column for each answer
                for a in q.answer_set.all():
                    columns.append(
                        Column(hierarchy=h, question=q, answer=a))
            else:
                columns.append(Column(hierarchy=h, question=q))
    return columns


def _get_quiz_results(h, s):
    quiz_type = ContentType.objects.filter(name='quiz')
    columns = []

    # quizzes
    for p in s.pageblock_set.filter(content_type=quiz_type):
        for q in p.block().question_set.all():
            if q.answerable() and q.is_multiple_choice():
                # need to make a column for each answer
                for a in q.answer_set.all():
                    columns.append(
                        Column(hierarchy=h, question=q, answer=a))
            else:
                columns.append(Column(hierarchy=h, question=q))

    return columns


def _get_career_location_results(h, s):
    careerlocation_type = ContentType.objects.filter(
        name='career location block')
    columns = []
    for p in s.pageblock_set.filter(content_type=careerlocation_type):
        if p.block().view == "IV":
            columns = iv_columns(p, h, columns)
        elif p.block().view == "LC":
            columns = lc_columns(h, columns)
        elif p.block().view == "BD":
            columns = boardmembers_columns(h, columns)

    return columns


def lc_columns(h, columns):
    # practice location - cell number
    columns.append(Column(hierarchy=h,
                   location="Practice Location Grid Number"))
    return columns


def boardmembers_columns(h, columns):
    # boardmembers
    for a in Actor.objects.filter(type="BD").order_by("order"):
        columns.append(Column(hierarchy=h, actor=a))
    # notes
    columns.append(Column(hierarchy=h, notes="Interview Notes"))
    return columns


def iv_columns(p, h, columns):
    # career location state
    for a in p.block().stakeholders:
        for q in a.questions.all():
            columns.append(Column(hierarchy=h, actor=a, actor_question=q))
    return columns


def _get_career_location_key(h, s):
    careerlocation_type = ContentType.objects.filter(
        name='career location block')
    columns = []

    for p in s.pageblock_set.filter(content_type=careerlocation_type):
        if p.block().view == "IV":
            columns = iv_columns(p, h, columns)
        elif p.block().view == "LC":
            columns = lc_columns(h, columns)
        elif p.block().view == "BD":
            # board members
            for a in Actor.objects.filter(type="BD").order_by("order"):
                for q in a.questions.all():
                    columns.append(Column(
                        hierarchy=h, actor=a, actor_question=q))

            # notes
            columns.append(
                Column(hierarchy=h, notes="Interview Notes"))

    return columns


def _get_career_strategy_results(h, s):
    careerstrategy_type = ContentType.objects.filter(
        name='career location strategy block')
    columns = []

    for p in s.pageblock_set.filter(content_type=careerstrategy_type):
        if p.block().view == "SS":
            columns.append(Column(hierarchy=h,
                                  strategy="Select a strategy"))
            for s in Strategy.objects.all():
                columns.append(Column(hierarchy=h,
                                      strategy=s,
                                      actor_question=s.question))

        elif p.block().view == "DS":
            for a in Actor.objects.filter(type="DS").order_by("order"):
                for q in a.questions.all():
                    columns.append(Column(
                        hierarchy=h, actor=a, actor_question=q))

    return columns


def _get_career_strategy_key(h, s):
    careerstrategy_type = ContentType.objects.filter(
        name='career location strategy block')
    columns = []

    for p in s.pageblock_set.filter(content_type=careerstrategy_type):
        if p.block().view == "SS":
            for s in Strategy.objects.all():
                columns.append(Column(hierarchy=h,
                                      strategy=s))
            for s in Strategy.objects.all():
                columns.append(Column(hierarchy=h,
                                      strategy=s,
                                      actor_question=s.question))

        elif p.block().view == "DS":
            for a in Actor.objects.filter(type="DS").order_by("order"):
                for q in a.questions.all():
                    columns.append(Column(
                        hierarchy=h, actor=a, actor_question=q))
    return columns


@login_required
def all_results_key(request):
    """
        A "key" for all questions and answers in the system.
        * One row for short/long text questions
        * Multiple rows for single/multiple-choice questions.
        Each question/answer pair get a row
        itemIdentifier - unique system identifier,
            concatenates hierarchy id, item type string,
            page block id (if necessary) and item id
        module - first child label in the hierarchy
        itemType - [question, discussion topic, referral field]
        itemText - identifying text for the item
        answerIdentifier - for single/multiple-choice questions. an answer id
        answerText
    """

    if not request.user.is_staff:
        return HttpResponseForbidden()

    response = HttpResponse(mimetype='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename=pass_response_key.csv'
    writer = csv.writer(response)
    headers = ['itemIdentifier', 'module', 'itemType', 'itemText',
               'answerIdentifier', 'answerText']
    writer.writerow(headers)

    columns = []
    for h in Hierarchy.objects.all():
        columns = columns + [Column(hierarchy=h)]
        for s in h.get_root().get_descendants():
            columns = columns + _get_quiz_key(h, s)
            columns = columns + _get_career_location_key(h, s)
            columns = columns + _get_career_strategy_key(h, s)

    for column in columns:
        try:
            writer.writerow(column.key_row())
        except:
            pass

    return response


@login_required
@rendered_with("main/all_results.html")
def all_results(request):
    """
        All system results
        * One or more column for each question in system.
            ** 1 column for short/long text. label = itemIdentifier from key
            ** 1 column for single choice. label = itemIdentifier from key
            ** n columns for multiple choice: 1 column for each possible answer
               *** column labeled as itemIdentifer_answer.id

        * One row for each user in the system.
            1. username
            2 - n: answers
                * short/long text. text value
                * single choice. answer.id
                * multiple choice.
                    ** answer id is listed in each question/answer
                    column the user selected
                * Unanswered fields represented as an empty cell
    """

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if not request.GET.get('format', 'html') == 'csv':
        return dict()

    columns = []
    for h in Hierarchy.objects.all():
        columns = columns + [Column(hierarchy=h)]
        for s in h.get_root().get_descendants():
            columns = columns + _get_quiz_results(h, s)
            columns = columns + _get_career_location_results(h, s)
            columns = columns + _get_career_strategy_results(h, s)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pass_responses.csv'
    writer = csv.writer(response)

    headers = ['userIdentifier', 'userEmail']
    for c in columns:
        headers += c.header_column()
    writer.writerow(headers)

    # Only look at users who have submission
    users = User.objects.filter(submission__isnull=False).distinct()
    for u in users:
        row = [u.username, u.email]
        for column in columns:
            v = smart_str(column.user_value(u))
            row.append(v)

        writer.writerow(row)

    return response


@login_required
@rendered_with('main/edit_page.html')
def edit_page(request, hierarchy, path):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    section = get_section_from_path(path, hierarchy)
    root = section.hierarchy.get_root()
    return dict(section=section,
                can_edit=True,
                module=get_module(section),
                modules=root.get_children(),
                root=section.hierarchy.get_root())


@login_required
def exporter(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    hierarchy = request.get_host()
    section = get_section_from_path('/', hierarchy=hierarchy)
    zip_filename = export_zip(section.hierarchy)

    with open(zip_filename) as zipfile:
        resp = HttpResponse(zipfile.read())
    resp['Content-Disposition'] = \
        "attachment; filename=%s.zip" % section.hierarchy.name

    os.unlink(zip_filename)
    return resp


@rendered_with("main/import.html")
@login_required
def importer(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "GET":
        return {}
    f = request.FILES['file']
    zipfile = ZipFile(f)

    # If we exported the morx.com site, and we are now
    # visiting http://fleem.com/import/, we don't want
    # to touch the morx.com hierarchy -- instead we want
    # to import the bundle to the fleem.com hierarchy.
    hierarchy_name = request.get_host()
    hierarchy = import_zip(zipfile, hierarchy_name)

    url = hierarchy.get_absolute_url()
    url = '/' + url.lstrip('/')  # sigh
    return HttpResponseRedirect(url)


def demographic_survey_complete(request):
    if request.user.is_anonymous():
        return False

    try:
        # Show the demographic survey if the user has not yet completed
        hierarchy = Hierarchy.objects.get(name='demographic')
    except Hierarchy.DoesNotExist:
        return HttpResponseServerError('Server does not have required data')

    section = hierarchy.get_section_from_path('survey')
    content_type = ContentType.objects.filter(name='quiz')
    registration_quiz = section.pageblock_set.filter(content_type=content_type)

    if len(registration_quiz) > 0:
        submission = Submission.objects.filter(
            quiz=registration_quiz[0].content_object, user=request.user)
        if len(submission) > 0:
            return True

    return False


def clear_state(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    try:
        request.user.get_profile().delete()
    except UserProfile.DoesNotExist:
        pass

    UserVisited.objects.filter(user=request.user).delete()

    # clear quiz
    import quizblock
    submissions = quizblock.models.Submission.objects.filter(user=request.user)
    submissions.delete()

    # clear careerlocationstate
    ActorResponse.objects.filter(user=request.user).delete()
    CareerLocationState.objects.filter(
        user=request.user).delete()
    SupportServiceState.objects.filter(
        user=request.user).delete()
    return HttpResponseRedirect("/")


@login_required
def download(request, filename):
    path = "%s/pdf/" % (settings.MEDIA_ROOT)
    full_path = os.path.join(path, filename)
    wrapper = FileWrapper(file(full_path))
    response = HttpResponse(wrapper, content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response['Content-Transfer-Encoding'] = 'binary'
    response['Accept-Ranges'] = 'bytes'
    response['Content-Encoding'] = 'none'
    response['Content-Length'] = os.path.getsize(full_path)
    return response
