from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render_to_response
from pagetree.helpers import get_hierarchy, get_section_from_path, get_module, needs_submit, submitted
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import *
from restclient import GET
import httplib2
import simplejson
from django.conf import settings
from munin.helpers import muninview
from pagetree.models import Section
from pagetree_export.exportimport import export_zip, import_zip
from pageblocks.exportimport import *
from quizblock.exportimport import *
import os

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

@rendered_with('main/page.html')
def page(request,path):
    hierarchy = request.get_host()
    section = get_section_from_path(path,hierarchy=hierarchy)

    root = section.hierarchy.get_root()
    module = get_module(section)

    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            return HttpResponseRedirect(section.get_next().get_absolute_url())

    if request.method == "POST":
        # user has submitted a form. deal with it
        if request.POST.get('action','') == 'reset':
            section.reset(request.user)
            return HttpResponseRedirect(section.get_absolute_url())
        proceed = section.submit(request.POST,request.user)
        if proceed:
            return HttpResponseRedirect(section.get_next().get_absolute_url())
        else:
            # giving them feedback before they proceed
            return HttpResponseRedirect(section.get_absolute_url())
    else:
        instructor_link = has_responses(section)
        return dict(section=section,
                    module=module,
                    needs_submit=needs_submit(section),
                    is_submitted=submitted(section,request.user),
                    modules=root.get_children(),
                    root=section.hierarchy.get_root(),
                    instructor_link=instructor_link,
                    )
@login_required
@rendered_with("main/instructor_page.html")
def instructor_page(request,path):
    h = get_hierarchy(request.get_host())
    section = get_section_from_path(path,hierarchy=h)
    root = section.hierarchy.get_root()
    module = get_module(section)

    quizzes = [p.block() for p in section.pageblock_set.all() if hasattr(p.block(),'needs_submit') and p.block().needs_submit()]
    return dict(section=section,
                quizzes=quizzes,
                module=get_module(section),
                modules=root.get_children(),
                root=h.get_root())

@login_required
@rendered_with('main/edit_page.html')
def edit_page(request,path):
    hierarchy = request.get_host()
    section = get_section_from_path(path,hierarchy=hierarchy)
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


