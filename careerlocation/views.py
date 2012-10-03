from django.http import HttpResponseRedirect, HttpResponseForbidden
from main.models import UserVisited
from pagetree.models import Hierarchy

def clear_state(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden

    hierarchy = Hierarchy.objects.get(name="module-two")
    UserVisited.objects.filter(user=request.user, section__hierarchy=hierarchy).delete()

    # clear careerlocationstate
    import careerlocation
    careerlocation.models.ActorResponse.objects.filter(user=request.user).delete()
    careerlocation.models.CareerLocationState.objects.filter(user=request.user).delete()

    return HttpResponseRedirect("/")

