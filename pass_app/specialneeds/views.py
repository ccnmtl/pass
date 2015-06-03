from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from pass_app.mixins import JSONResponseMixin
from pass_app.specialneeds.models import SpecialNeedsCall, \
    SpecialNeedsCallState


class SpecialNeedsSaveStateView(JSONResponseMixin, View):
    def post(self, request):
        state, created = SpecialNeedsCallState.objects.get_or_create(
            user=request.user)
        item_id = request.POST.get('item_id', None)
        item = get_object_or_404(SpecialNeedsCall, id=item_id)
        state.questions.add(item)
        ctx = {'success': True}
        return self.render_to_json_response(ctx)
