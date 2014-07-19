from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from pass_app.infographic.models import InfographicItem, InfographicItemForm, \
    InfographicBlock


class InfographicDetailView(DetailView):
    model = InfographicBlock


class CreateInfographicItemView(CreateView):
    form_class = InfographicItemForm
    model = InfographicItem

    def get_success_url(self):
        return "/_infographic/%s/" % self.object.infographic.id

    def get_initial(self):
        infographic = get_object_or_404(InfographicBlock,
                                        pk=self.kwargs.get('pk'))
        return {'infographic': infographic}


class DeleteInfographicItemView(DeleteView):
    model = InfographicItem

    def get_success_url(self):
        return "/_infographic/%s/" % self.object.infographic.id


class UpdateInfographicItemView(UpdateView):
    form_class = InfographicItemForm
    model = InfographicItem

    def get_success_url(self):
        return "/_infographic/%s/" % self.object.infographic.id
