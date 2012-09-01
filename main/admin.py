from main.models import UserVisited
from django.contrib import admin

class UserVisitedAdmin(admin.ModelAdmin):
    class Meta:
        model = UserVisited

    search_fields = ["user__user__username"]
    list_display = ("user","section","visited_time")

admin.site.register(UserVisited, UserVisitedAdmin)

