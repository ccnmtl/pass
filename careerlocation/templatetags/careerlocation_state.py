from django import template
from careerlocation.models import CareerLocationState
register = template.Library()

@register.filter('notepad')
def notepad(user):
    state, create = CareerLocationState.objects.get_or_create(user=user)
    return state.notes

class GetUserStateId(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        u = self.user.resolve(context)

        obj, create = CareerLocationState.objects.get_or_create(user=u)
        return obj.id

@register.tag('get_user_state_id')
def get_user_state_id(parser, token):
    user = token.split_contents()[1:][0]
    return GetUserStateId(user)

class GetUserResponse(template.Node):
    def __init__(self, user, question):
        self.user = template.Variable(user)
        self.question = template.Variable(question)

    def render(self, context):
        u = self.user.resolve(context)
        q = self.question.resolve(context)

        obj, create = CareerLocationState.objects.get_or_create(user=u)

        response = obj.get_response(q)
        return response

@register.tag('get_user_response')
def get_user_response(parser, token):
    user = token.split_contents()[1:][0]
    question = token.split_contents()[1:][1]

    return GetUserResponse(user, question)

