from models import CareerMap, Question, Layer, Response, BaseMap

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

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

@rendered_with('careermapblock/edit_layers.html')
def edit_layers(request,id):
    cmap = get_object_or_404(CareerMap,id=id)
    section = cmap.pageblock().section
    return dict(cmap=cmap,section=section)

@rendered_with('careermapblock/edit_basemaps.html')
def edit_basemaps(request,id):
    cmap = get_object_or_404(CareerMap,id=id)
    section = cmap.pageblock().section
    return dict(cmap=cmap,section=section)

@rendered_with('careermapblock/edit_questions.html')
def edit_questions(request,id):
    cmap = get_object_or_404(CareerMap,id=id)
    section = cmap.pageblock().section
    return dict(cmap=cmap,section=section)

def delete_question(request,id):
    question = get_object_or_404(Question,id=id)
    if request.method == "POST":
        cmap = question.cmap
        question.delete()
        return HttpResponseRedirect(reverse("edit-careermap-questions",args=[cmap.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")

def reorder_questions(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this", status=400)
    cmap = get_object_or_404(CareerMap,id=id)
    keys = request.GET.keys()
    question_keys = [int(k[len('question_'):]) for k in keys if k.startswith('question_')]
    question_keys.sort()
    questions = [int(request.GET['question_' + str(k)]) for k in question_keys]
    cmap.update_questions_order(questions)
    return HttpResponse("ok")


def add_question(request,id):
    cmap = get_object_or_404(CareerMap,id=id)
    form = cmap.add_question_form(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        question.cmap = cmap
        question.save()
    return HttpResponseRedirect(reverse("edit-careermap-questions",args=[cmap.id]))

@rendered_with('careermapblock/edit_question.html')
def edit_question(request,id):
    question = get_object_or_404(Question,id=id)
    if request.method == "POST":
        form = question.edit_form(request.POST)
        question = form.save(commit=False)
        question.save()
        return HttpResponseRedirect(reverse("edit-careermap-question",args=[question.id]))
    return dict(question=question)


def delete_layer(request,id):
    layer = get_object_or_404(Layer,id=id)
    if request.method == "POST":
        cmap = layer.cmap
        layer.delete()
        return HttpResponseRedirect(reverse("edit-careermap-layers",args=[cmap.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")

def reorder_layers(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this", status=400)
    cmap = get_object_or_404(CareerMap,id=id)
    keys = request.GET.keys()
    layer_keys = [int(k[len('layer_'):]) for k in keys if k.startswith('layer_')]
    layer_keys.sort()
    layers = [int(request.GET['layer_' + str(k)]) for k in layer_keys]
    cmap.update_layers_order(layers)
    return HttpResponse("ok")


def add_layer(request,id):
    cmap = get_object_or_404(CareerMap,id=id)
    form = cmap.add_layer_form(request.POST,request.FILES)
    if form.is_valid():
        layer = form.save(commit=False)
        layer.cmap = cmap
        layer.save()
    else:
        print "form was not valid"
        print form.errors
    return HttpResponseRedirect(reverse("edit-careermap-layers",args=[cmap.id]))

@rendered_with('careermapblock/edit_layer.html')
def edit_layer(request,id):
    layer = get_object_or_404(Layer,id=id)
    if request.method == "POST":
        form = layer.edit_form(request.POST)
        layer = form.save(commit=False)
        layer.save()
        return HttpResponseRedirect(reverse("edit-careermap-layer",args=[layer.id]))
    return dict(layer=layer)


def delete_basemap(request,id):
    basemap = get_object_or_404(BaseMap,id=id)
    if request.method == "POST":
        cmap = basemap.cmap
        basemap.delete()
        return HttpResponseRedirect(reverse("edit-careermap-basemaps",args=[cmap.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")

def reorder_basemaps(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this", status=400)
    cmap = get_object_or_404(CareerMap,id=id)
    keys = request.GET.keys()
    basemap_keys = [int(k[len('basemap_'):]) for k in keys if k.startswith('basemap_')]
    basemap_keys.sort()
    basemaps = [int(request.GET['basemap_' + str(k)]) for k in basemap_keys]
    cmap.update_basemaps_order(basemaps)
    return HttpResponse("ok")


def add_basemap(request,id):
    cmap = get_object_or_404(CareerMap,id=id)
    form = cmap.add_basemap_form(request.POST,request.FILES)
    if form.is_valid():
        basemap = form.save(commit=False)
        basemap.cmap = cmap
        basemap.save()
    else:
        print "form was not valid"
        print form.errors
    return HttpResponseRedirect(reverse("edit-careermap-basemaps",args=[cmap.id]))

@rendered_with('careermapblock/edit_basemap.html')
def edit_basemap(request,id):
    basemap = get_object_or_404(BaseMap,id=id)
    if request.method == "POST":
        form = basemap.edit_form(request.POST)
        basemap = form.save(commit=False)
        basemap.save()
        return HttpResponseRedirect(reverse("edit-careermap-basemap",args=[basemap.id]))
    return dict(basemap=basemap)

