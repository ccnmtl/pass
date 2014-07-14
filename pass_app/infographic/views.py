from models import (InfographicBlock, InfographicItem, InfographicForm,
                    InfographicItemForm)
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView


class EditInfographicView(DetailView):
    model = InfographicBlock


class DeleteInfographicItemView(DeleteView):
    model = InfographicItem


class CreateInfographicItemView(CreateView):
    form_class = InfographicItemForm
    model = InfographicItem


class UpdateInfographicItemView(UpdateView):
    form_class = InfographicItemForm
    model = InfographicItem
