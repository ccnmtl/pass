from django import template

from pass_app.specialneeds.models import \
    SpecialNeedsCallState, SpecialNeedsCall


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_user_state(context, item):
    if 'user' not in context:
        return SpecialNeedsCall.objects.none()

    obj, create = SpecialNeedsCallState.objects.get_or_create(
        user=context['user'])
    return obj.questions.filter(id=item.id).count() > 0
