from django import template
from pass_app.specialneeds.models import SpecialNeedsCallState


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_user_state(context, item):
    obj, create = SpecialNeedsCallState.objects.get_or_create(
        user=context['user'])
    return obj.questions.filter(id=item.id).count() > 0
