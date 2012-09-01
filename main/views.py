from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.encoding import smart_str
from pagetree.helpers import get_hierarchy, get_section_from_path, get_module, needs_submit, submitted
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from models import *
from pagetree.models import Hierarchy
from pagetree_export.exportimport import export_zip, import_zip
from quizblock.models import Submission, Response
from main.models import UserProfile
import os
import csv
import django.core.exceptions

def get_or_create_profile(user,section):
    if user.is_anonymous():
        return None
    try:
        user_profile,created = UserProfile.objects.get_or_create(user=user)
    except django.core.exceptions.MultipleObjectsReturned:
        user_profile = UserProfile.objects.filter(user=user)[0]
        created = False
    if created:
        first_leaf = section.hierarchy.get_first_leaf(section)
        ancestors = first_leaf.get_ancestors()
        for a in ancestors:
            user_profile.save_visit(a)
    return user_profile

def _unlocked(profile,section):
    """ if the user can proceed past this section """
    if profile is None:
        return False
    if not section:
        return True
    if section.is_root() or not section.is_leaf():
        return True
    if profile.has_visited(section):
        return True

    previous = section.get_previous()
    if not previous:
        return True
    else:
        if not profile.has_visited(previous):
            return False

    # if the previous page had blocks to submit
    # we only let them by if they submitted
    for p in previous.pageblock_set.all():
        if hasattr(p.block(),'unlocked'):
            if not p.block().unlocked(profile.user):
                return False
          
    return profile.has_visited(previous)


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items
        return rendered_func

def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all() if hasattr(p.block(),'needs_submit') and p.block().needs_submit()]
    return quizzes != []

def allow_redo(section):
    """ if blocks on the page allow redo """
    allowed = True
    for p in section.pageblock_set.all():
        if hasattr(p.block(),'allow_redo'):
            if not p.block().allow_redo:
                allowed = False
    return allowed

@rendered_with('main/intro.html')
def intro(request):
    return { 'demographic_survey_complete': demographic_survey_complete(request) }

@login_required
@rendered_with('main/page.html')
def demographic(request,path):
    hierarchy = get_hierarchy('Demographic')
    return process_page(request,path,hierarchy)

@login_required
@rendered_with('main/page.html')
def module_one(request,path):
    if not demographic_survey_complete(request):
        hierarchy = get_hierarchy('Demographic')
        return HttpResponseRedirect(hierarchy.get_root().get_absolute_url())

    hierarchy = get_hierarchy('Module One')
    return process_page(request,path,hierarchy)

@login_required
@rendered_with('main/page.html')
def module_two(request,path):
    if not demographic_survey_complete(request):
        hierarchy = get_hierarchy('Demographic')
        return HttpResponseRedirect(hierarchy.get_root().get_absolute_url())

    hierarchy = get_hierarchy('Module Two')
    return process_page(request,path,hierarchy)

@login_required
@rendered_with('main/page.html')
def process_page(request,path,hierarchy):
    section = get_section_from_path(path,hierarchy=hierarchy)

    root = hierarchy.get_root()
    module = get_module(section)

    user_profile = get_or_create_profile(user=request.user,section=section)
    can_access = _unlocked(user_profile,section)
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
        # user has submitted a form. deal with it
        if request.POST.get('action','') == 'reset':
            section.reset(request.user)
            return HttpResponseRedirect(section.get_absolute_url())

        section.submit(request.POST,request.user)

        if hierarchy.name == 'Demographic' and path.startswith("survey"):
            return HttpResponseRedirect("/")

        next = section.get_next()
        if next:
            # ignoring proceed and always pushing them along. see PMT #77454
            return HttpResponseRedirect(section.get_next().get_absolute_url())
        else:
            return HttpResponseRedirect("/")
    else:
        instructor_link = has_responses(section)
        allow_next_link = not needs_submit(section) or submitted(section,request.user)
        end_section = section.get_next()
        return dict(section=section,
                    module=module,
                    allow_next_link=allow_next_link,
                    needs_submit=needs_submit(section),
                    is_submitted=submitted(section,request.user),
                    modules=root.get_children(),
                    root=section.hierarchy.get_root(),
                    instructor_link=instructor_link,
                    can_edit=can_edit,
                    allow_redo=allow_redo(section),
                    next_unlocked = _unlocked(user_profile,section.get_next()),
                    )
@login_required
@rendered_with("main/instructor_page.html")
def instructor_page(request,path):
    h = get_hierarchy(request.get_host())
    section = get_section_from_path(path,hierarchy=h)
    root = section.hierarchy.get_root()
    module = get_module(section)

    if request.method == "POST":
        if 'clear' in request.POST.keys():
            submission = get_object_or_404(Submission,id=request.POST['clear'])
            submission.delete()
            return HttpResponseRedirect("/instructor" + section.get_absolute_url())

    quizzes = [p.block() for p in section.pageblock_set.all() if hasattr(p.block(),'needs_submit') and p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                modules=root.get_children(),
                root=h.get_root())


@login_required
@rendered_with("main/all_results.html")
def all_results(request):

    if not request.user.is_superuser():
        return HttpResponseForbidden()

    h = get_hierarchy(request.get_host())
    all_users = User.objects.all()
    quizzes = []
    for s in h.get_root().get_descendants():
        for p in s.pageblock_set.all():
            if hasattr(p.block(),'needs_submit') and p.block().needs_submit():
                quizzes.append(p)

    questions = []
    for qz in quizzes:
        for q in qz.block().question_set.all():
            questions.append(q)

    class Column(object):
        def __init__(self,question=None,answer=None):
            self.question = question
            self.answer = answer
            self._label_cache = None

        def label(self):
            # don't want to have to recompute the labels on every row
            if self._label_cache is None:
                if self.answer is None:
                    self._label_cache = "%d%s%s/%s" % (self.question.id,self.question.quiz.pageblock().section.get_absolute_url(),
                                                     self.question.quiz.pageblock().label,
                                                     self.question.text)
                else:
                    self._label_cache = "%d%s%s/%s/%s" % (self.question.id,self.question.quiz.pageblock().section.get_absolute_url(),
                                                          self.question.quiz.pageblock().label,
                                                          self.question.text,self.answer.label)
            return self._label_cache

        def value(self,user):
            r = Submission.objects.filter(quiz=self.question.quiz,user=user).order_by("-submitted")
            if r.count() == 0:
                # user has not submitted this form
                return ""
            submission = r[0]
            r = Response.objects.filter(question=self.question,submission=submission)
            if r.count() > 0:
                if self.answer is None:
                    # text/short answer type question
                    return r[0].value
                else:
                    # multiple/single choice
                    if self.answer.value in [res.value for res in self.question.user_responses(user)]:
                        return "1"
                    else:
                        return "0"
            else:
                # user submitted this form, but left this question blank somehow
                return ""

    columns = []
    for q in questions:
        if q.answerable():
            # need to make a column for each answer
            for a in q.answer_set.all():
                columns.append(Column(question=q,answer=a))
        else:
            columns.append(Column(question=q))

    all_responses = []
    for u in all_users:
        row = []
        for column in columns:
            v = column.value(u)
            row.append(v)
        all_responses.append(dict(user=u,row=row))

    def clean_header(s):
        s = s.replace('<div class=\'question-sub\'>','')
        s = s.replace('<div class=\'question\'>','')
        s = s.replace('<p>','')
        s = s.replace('</p>','')
        s = s.replace('</div>','')
        s = s.replace('\n','')
        s = s.replace('\r','')
        s = s.replace('<','')
        s = s.replace('>','')
        s = s.replace('\'','')
        s = s.replace('\"','')
        s = s.replace(',','')
        return s

    if request.GET.get('format','html') == 'csv':
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=pass_responses.csv'
        writer = csv.writer(response)
        headers = ['user'] + ["%s" % clean_header(c.label().encode('utf-8')) for c in columns]
        writer.writerow(headers)
        for r in all_responses:
            rd = [smart_str(c) for c in [r['user'].username] + r['row']]
            assert len(rd) == len(headers)
            writer.writerow(rd)
        return response
    else:
        return dict(all_columns=columns,all_responses=all_responses)

@login_required
@rendered_with('main/edit_page.html')
def edit_page(request,path):
    hierarchy_name,slash,section_path = path.partition('/')
    section = get_section_from_path(section_path,hierarchy=hierarchy_name)

    root = section.hierarchy.get_root()
    module = get_module(section)

    return dict(section=section,
        module=get_module(section),
        modules=root.get_children(),
        root=section.hierarchy.get_root())


@login_required
def exporter(request):
    hierarchy = request.get_host()
    section = get_section_from_path('/', hierarchy=hierarchy)
    zip_filename = export_zip(section.hierarchy)

    with open(zip_filename) as zipfile:
        resp = HttpResponse(zipfile.read())
    resp['Content-Disposition'] = "attachment; filename=%s.zip" % section.hierarchy.name

    os.unlink(zip_filename)
    return resp

from zipfile import ZipFile

@rendered_with("main/import.html")
@login_required
def importer(request):
    if request.method == "GET":
        return {}
    file = request.FILES['file']
    zipfile = ZipFile(file)

    # If we exported the morx.com site, and we are now
    # visiting http://fleem.com/import/, we don't want
    # to touch the morx.com hierarchy -- instead we want
    # to import the bundle to the fleem.com hierarchy.
    hierarchy_name = request.get_host()
    hierarchy = import_zip(zipfile, hierarchy_name)

    url = hierarchy.get_absolute_url()
    url = '/' + url.lstrip('/') # sigh
    return HttpResponseRedirect(url)


def demographic_survey_complete(request):
    if request.user.is_anonymous():
        return False

    # Show the demographic survey if the user has not yet completed
    hierarchy = Hierarchy.objects.get(name='Demographic')
    section = hierarchy.get_section_from_path('survey')
    content_type = ContentType.objects.filter(name='quiz')
    registration_quiz = section.pageblock_set.filter(content_type=content_type)

    if len(registration_quiz) > 0:
        submission = Submission.objects.filter(quiz=registration_quiz[0].content_object, user=request.user)
        if len(submission) > 0:
            return True

    return False
