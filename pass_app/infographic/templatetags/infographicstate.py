from django import template
from pass_app.infographic.models import InfographicState


register = template.Library()


class GetUserState(template.Node):
    def __init__(self, block):
        self.block = block

    def render(self, context):
        b = context[self.block]
        u = context['request'].user

        obj, create = InfographicState.objects.get_or_create(user=u)
        return obj.items.filter(infographic=b).values_list('id', flat=True)


@register.tag('get_user_state')
def get_user_state(parser, token):
    block = token.split_contents()[1:][0]
    return GetUserState(block)
