from django import template
from pass_app.supportservices.models import SupportServiceState

register = template.Library()


class GetUserStateId(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        u = self.user.resolve(context)

        obj, created = SupportServiceState.objects.get_or_create(user=u)
        return obj.id


@register.tag('get_user_state_id')
def get_user_state_id(parser, token):
    user = token.split_contents()[1:][0]
    return GetUserStateId(user)
