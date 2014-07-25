from django import template
from pass_app.infographic.models import InfographicState


register = template.Library()


class GetUserState(template.Node):
    def render(self, context):
        u = context['request'].user

        obj, create = InfographicState.objects.get_or_create(user=u)
        return obj.items.values_list('id', flat=True)


@register.tag('get_user_state')
def get_user_state(parser, token):
    return GetUserState()
