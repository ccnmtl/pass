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

class LayerSelectedNode(template.Node):
    def __init__(self, layer, nodelist_true, nodelist_false=None):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.layer = layer

    def render(self, context):
        l = context[self.layer]
        r = context['request']

        state, create = CareerLocationState.objects.get_or_create(user=r.user)
        qs = state.selected_layers.filter(name=l.name)
        if len(qs) > 0:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

@register.tag('if_layer_selected')
def if_layer_selected(parser, token):
    layer = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else','endif_layer_selected'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_layer_selected',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return LayerSelectedNode(layer, nodelist_true, nodelist_false)

