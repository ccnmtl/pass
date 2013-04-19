from django import template
from pass_app.careerlocation.models import CareerLocationState, \
    CareerLocationBlock
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


class GetLocationCount(template.Node):
    def __init__(self, block, cells, row, column):
        self.block = template.Variable(block)
        self.cells = template.Variable(cells)
        self.row = template.Variable(row)
        self.column = template.Variable(column)

    def render(self, context):
        self.block.resolve(context)
        c = self.cells.resolve(context)
        x = self.column.resolve(context)
        y = self.row.resolve(context)

        columns = len(CareerLocationBlock.grid_columns)
        idx = (y * columns) + x
        return c[idx] if c[idx] else ""


@register.tag('get_location_count')
def get_location_count(parser, token):
    block = token.split_contents()[1:][0]
    cells = token.split_contents()[1:][1]
    row = token.split_contents()[1:][2]
    column = token.split_contents()[1:][3]

    return GetLocationCount(block, cells, row, column)


class GetCareerLocationState(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        u = self.user.resolve(context)

        obj, created = CareerLocationState.objects.get_or_create(user=u)
        return obj


@register.tag('get_career_location_state')
def get_career_location_state(parser, token):
    user = token.split_contents()[1:][0]
    return GetCareerLocationState(user)


class GetUserStrategyState(template.Node):
    def __init__(self, user, strategy):
        self.user = template.Variable(user)
        self.strategy = template.Variable(strategy)

    def render(self, context):
        u = self.user.resolve(context)
        s = self.strategy.resolve(context)

        obj, created = CareerLocationState.objects.get_or_create(user=u)
        if s == obj.strategy_selected:
            return "selected"
        elif s in obj.strategies_viewed.all():
            return "viewed"

        return ""


@register.tag('get_user_strategy_state')
def get_user_strategy_state(parser, token):
    user = token.split_contents()[1:][0]
    strategy = token.split_contents()[1:][1]
    return GetUserStrategyState(user, strategy)
