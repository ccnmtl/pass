from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class UsernameAuthorization(Authorization):

    def read_detail(self, object_list, bundle):
        lst = self.read_list(object_list, bundle)
        return len(lst) > 0

    def read_list(self, object_list, bundle):
        request = bundle.request
        if request and hasattr(request, 'user'):
            return object_list.filter(username=request.user.username)

        return object_list.none()


class UserAuthorization(Authorization):
    def read_detail(self, object_list, bundle):
        lst = self.read_list(object_list, bundle)
        return len(lst) > 0

    def read_list(self, object_list, bundle):
        request = bundle.request
        if request and hasattr(request, 'user'):
            return object_list.filter(user=request.user)

        return object_list.none()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser', 'date_joined']
        allowed_methods = ['get']
        authorization = UsernameAuthorization()
